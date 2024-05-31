import numpy as np
import cvxpy as cp
from tqdm import trange
from mip import Model, xsum, maximize
from ortools.linear_solver import pywraplp


def normalize(S: np.ndarray, base_val: float = 0) -> np.ndarray:
    S = S - np.min(S) + base_val
    S = S / (np.max(S) -  np.min(S))

    return S


def optimize(S: np.ndarray, k: int = 30, epsilon: int = 15) -> np.ndarray:
    n_user = S.shape[0]
    n_item = S.shape[1]

    model = Model()

    W = [[model.add_var() for j in range(n_item)] for i in range(n_user)]

    model.objective = maximize(
        xsum((S[i][j] * W[i][j]) for i in range(n_user) for j in range(n_item))
    )

    for i in range(n_user):
        model += xsum(W[i][j] for j in range(n_item)) == k

    for j in range(n_item):
        model += epsilon <= xsum(W[i][j] for i in range(n_user))

    for i in range(n_user):
        for j in range(n_item):
            model += W[i][j] <= 1

    model.optimize()

    W_np = np.array(
        [[W[i][j].x for j in range(S.shape[1])] for i in range(S.shape[0])]
    )
    return W_np


def optimizeORTools(S: np.ndarray, k: int = 30, epsilon: int = 5) -> np.ndarray:
    solver = pywraplp.Solver.CreateSolver("PDLP")

    if solver is None:
        return

    n_users, n_items = S.shape[:2]

    x = {}
    for i in range(n_users):
        for j in range(n_items):
            x[i, j] = solver.BoolVar(f"x_{i}_{j}")

    for i in range(n_users):
        solver.Add(sum(x[i, j] for j in range(n_items)) == k)

    for j in range(n_items):
        solver.Add(sum(x[i, j] for i in range(n_users)) >= epsilon)

    objective = solver.Objective()
    for i in range(n_users):
        for j in range(n_items):
            objective.SetCoefficient(x[i, j], int(S[i, j] * 1000))
    objective.SetMaximization()

    solver.Solve()

    W = np.array(
        [[x[i, j].solution_value() for j in range(n_items)] for i in range(n_users)]
    )
    return W


def get_item_provider_mapper(S: np.ndarray, p=0.05):
    items_count = np.sum(S, axis=0)
    items_id_sorted = np.argsort(items_count)

    item_interval = int(len(items_id_sorted) * p)
    item2provider = np.zeros(len(items_id_sorted), dtype=np.int32)
    for i, s in enumerate(range(0, len(items_id_sorted), item_interval)):
        item2provider[items_id_sorted[s : s + item_interval]] = i
    return item2provider


class UMMFReRanking():
    def relabel_provider(self, interactions, preference_scores=None, p=0.05):
        if preference_scores is not None:
            item2provider = get_item_provider_mapper(preference_scores, p)
            interactions[:, 3] = item2provider[interactions[:, 1]]

        interactions[:, 3] = np.unique(interactions[:, 3], return_inverse=True)[1]
        return interactions

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def cpu_layer(self, ordered_tilde_dual, rho, lambd):
        m = len(rho)
        answer = cp.Variable(m)
        objective = cp.Minimize(
            cp.sum_squares(
                cp.multiply(rho, answer) - cp.multiply(rho, ordered_tilde_dual)
            )
        )

        constraints = []
        for i in range(1, m + 1):
            constraints += [cp.sum(cp.multiply(rho[:i], answer[:i])) >= -lambd]
        prob = cp.Problem(objective, constraints)
        prob.solve()

        return answer.value

    def compute_next_dual(self, eta, rho, dual, gradient, lambd):
        tilde_dual = dual - eta * gradient / rho / rho
        order = np.argsort(tilde_dual * rho)
        ordered_tilde_dual = tilde_dual[order]
        ordered_next_dual = self.cpu_layer(ordered_tilde_dual, rho[order], lambd)
        return ordered_next_dual[order.argsort()]

    def optimize(self, S: np.ndarray, k: int = 30, p: float = 0.05, *args, **kargs) -> np.ndarray:
        lambd = kargs.get("lambd", 0.1)
        alpha = kargs.get("alpha", 0.1)
        eta = kargs.get("eta", 1e-3)

        n_users, n_items = S.shape[:2]
        item2provider = get_item_provider_mapper(S, p)

        n_providers = len(np.unique(item2provider))
        providers_cnt = np.unique(item2provider, return_counts=True)[1]

        rho = (1 + 1 / n_providers) * providers_cnt / np.sum(providers_cnt)
        UI_matrix = S[np.arange(n_users)]

        # normalize user-item perference score to [0,1]
        UI_matrix = self.sigmoid(UI_matrix)

        # set item-provider matrix
        A = np.zeros((n_items, n_providers))
        iid2pid = []
        for i in range(n_items):
            iid2pid.append(item2provider[i])
            A[i, item2provider[i]] = 1


        result_x = []

        mu_t = np.zeros(n_providers)
        B_t = n_users * k * rho
        sum_dual = 0
        eta_t = eta / np.sqrt(n_users)
        gradient_cusum = np.zeros(n_providers)
        for t in trange(n_users):
            x_title = UI_matrix[t, :] - np.matmul(A, mu_t)
            mask = np.matmul(A, (B_t > 0).astype(np.float32))

            mask = (1.0 - mask) * -10000.0
            x = np.argsort(x_title + mask, axis=-1)[::-1]
            x_allocation = x[:k]
            re_allocation = np.argsort(UI_matrix[t, x_allocation])[::-1]
            x_allocation = x_allocation[re_allocation]
            result_x.append(x_allocation)

            B_t = B_t - np.sum(A[x_allocation], axis=0, keepdims=False)
            gradient = -np.mean(A[x_allocation], axis=0, keepdims=False) + B_t / (
                n_users * k
            )

            gradient = alpha * gradient + (1 - alpha) * gradient_cusum
            gradient_cusum = gradient
            mu_t = self.compute_next_dual(eta_t, rho, mu_t, gradient, lambd)
            sum_dual += mu_t


        W = np.zeros((n_users, n_items))
        for i in range(n_users):
            W[i, result_x[i]] = 1

        return W

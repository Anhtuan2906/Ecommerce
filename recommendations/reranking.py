import numpy as np
from mip import Model, xsum, maximize



def optimize(self, S: np.ndarray, k: int = 30, epsilon: int = 15) -> np.ndarray:
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

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from ecommerce.utils import require_login
from .models import User
from .forms import LoginForm, RegisterForm

HOMEPAGE = 'store:products'


# Create your views here.
def signin(request):
    if request.user.is_authenticated:
        return redirect(HOMEPAGE)

    if request.method == 'GET':
        return render(
            request,
            'customers/login.html',
            {'form': LoginForm(), 'message': '', 'is_error': False},
        )

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(HOMEPAGE)
            else:
                return render(
                    request,
                    'customers/login.html',
                    {
                        'form': form,
                        'message': 'Invalid username or password',
                        'is_error': True,
                    },
                )
        else:
            return render(
                request,
                'customers/login.html',
                {'form': form, 'message': form.errors, 'is_error': True},
            )

    return HttpResponse(status=400)


@require_login
def signout(request):
    logout(request)
    return redirect('customers:login')


def register(request):
    if request.user.is_authenticated:
        return redirect(HOMEPAGE)

    if request.method == 'GET':
        return render(
            request,
            'customers/register.html',
            {'form': RegisterForm(), 'message': '', 'is_error': False},
        )

    if request.method == 'POST':
        data = request.POST.dict()
        if 'email' in data:
            data['username'] = data['email']
        form = RegisterForm(data)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if password != password2:
                return render(
                    request,
                    'customers/register.html',
                    {
                        'form': form,
                        'message': 'Passwords do not match',
                        'is_error': True,
                    },
                )

            if User.objects.filter(username=email).exists():
                return render(
                    request,
                    'customers/register.html',
                    {'form': form, 'message': 'Email already exists', 'is_error': True},
                )

            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,
            )

            return render(request, 'customers/register_success.html')
        else:
            return render(
                request,
                'customers/register.html',
                {'form': form, 'message': form.errors, 'is_error': True},
            )

    return HttpResponse(status=400)

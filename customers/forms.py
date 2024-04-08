from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=64)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=64)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=64)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

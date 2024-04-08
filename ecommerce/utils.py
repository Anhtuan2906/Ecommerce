from django.shortcuts import redirect


def require_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("customers:login")
        return view(request, *args, **kwargs)

    return new_view

from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages

User = get_user_model()

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        if not username or not password:
            messages.add_message(request, messages.WARNING, "You haven't entered username or password.", extra_tags="text text-warning")
            return render(request, "auth/login.html")
        
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.add_message(request, messages.ERROR, "Username or password is incorrect.", extra_tags="text text-danger")
            return render(request, "auth/login.html")
        
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "You have successfully logged in!", extra_tags="text text-success")
        return redirect("list_of_urls")

    return render(request, "auth/login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password1 = request.POST.get("password1", None)
        password2 = request.POST.get("password2", None)

        if not username or not password1 or not password2:
            messages.add_message(request, messages.WARNING, "You haven't entered username or password.", extra_tags="text text-warning")
            return render(request, "auth/register.html")
        
        if password1.strip() != password2.strip():
            messages.add_message(request, messages.WARNING, "Passwords don't match.", extra_tags="text text-warning")
            return render(request, "auth/register.html")
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.WARNING, "This username already exists.", extra_tags="text text-warning")
            return render(request, "auth/register.html")

        User.objects.create_user(username=username, password=password1.strip())

        messages.add_message(request, messages.SUCCESS, "You have successfully registered!", extra_tags="text text-success")
        return redirect("login_user")

    return render(request, "auth/register.html")


def logout_user(request):
    logout(request)
    return redirect("login_user")
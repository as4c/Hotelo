
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import get_user_model,login,authenticate,logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from auth_app.forms import UserRegistrationForm, UserEditForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.views.generic import UpdateView


User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # log the user in
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:home")
        else:
            return render(request, "signin.html", {"error": "Invalid email or password."})
    else:
        return render(request, "signin.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("signin")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'edit_profile.html', {'user_form': user_form})

@require_http_methods(["GET", "POST"])
def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "example.com",
                        "site_name": "Example",
                        "uid": str(user.id),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, None, [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponseBadRequest(str(e))
                return redirect("password_reset_done")
            else:
                return render(request, "password_reset.html", {"error": "No user with that email found."})
    else:
        form = PasswordResetForm()
    return render(request, "password_reset.html", {"form": form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")
    form_class = SetPasswordForm


@login_required
def profile(request):
    user = request.user
    return render(request, "profile.html", {"user": user})

class CustomUserUpdateView(UpdateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "update_profile.html"
    success_url = reverse_lazy("profile")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.id == int(kwargs["pk"]):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to edit this user's profile.")

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs["pk"])

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)


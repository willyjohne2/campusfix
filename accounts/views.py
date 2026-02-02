from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import (
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

try:
    from django_ratelimit.decorators import ratelimit
except Exception:
    # fallback for alternative package names
    from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.views import View
from .forms import (
    RegistrationForm,
    LoginForm,
    PasswordResetForm,
    PasswordResetCodeForm,
    SuperAdminLoginForm,
)
from .models import Profile, SuperAdmin
from .forms import EmailVerificationForm
from .models import EmailVerification
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta
from .models import PasswordResetCode
from .email_utils import send_verification_email, send_password_reset_email
from .forms import ReplyForm
from .models import ContactMessage, ContactReply
from .email_utils import send_reply_email
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import check_password


@ensure_csrf_cookie
def register(request):
    """
    User registration view
    Fields: name, email, password1, password2
    Creates user and associated profile
    """
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.profile.is_admin():
            return redirect("admin_dashboard_overview")
        return redirect("dashboard_home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated profile with unverified status
            Profile.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                is_verified=False,
            )

            # Generate verification code
            code = EmailVerification.generate_code()
            expires = timezone.now() + timedelta(hours=24)
            EmailVerification.objects.create(user=user, code=code, expires_at=expires)

            # Send verification email via Brevo
            send_verification_email(user.email, code)

            messages.success(
                request,
                "Account created successfully! A verification code has been sent to your email. Please check your inbox.",
            )
            return redirect("verify_email")
        else:
            # Form has errors, re-render with error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@ensure_csrf_cookie
@ratelimit(key="ip", rate="10/m", block=True)
def login_view(request):
    """
    User login view
    Authenticates using email and password
    Supports "Remember Me" checkbox to extend session timeout
    """
    if request.user.is_authenticated:
        return login_redirect(request)

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        remember_me = request.POST.get("remember_me")

        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return render(request, "accounts/login.html")

        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Prevent login until email is verified
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = None

            if profile and not profile.is_verified:
                messages.info(
                    request,
                    "Please verify your email before logging in. Check your inbox for the code.",
                )
                # Ensure a verification object exists (create if missing)
                if not EmailVerification.objects.filter(
                    user=user, expires_at__gt=timezone.now()
                ).exists():
                    code = EmailVerification.generate_code()
                    expires = timezone.now() + timedelta(hours=24)
                    EmailVerification.objects.create(
                        user=user, code=code, expires_at=expires
                    )
                    # attempt to resend
                    try:
                        send_mail(
                            "CampusFix Email Verification",
                            f"Your CampusFix verification code is: {code}",
                            getattr(settings, "DEFAULT_FROM_EMAIL", None),
                            [user.email],
                            fail_silently=True,
                        )
                    except Exception:
                        pass
                return redirect("verify_email")

            login(request, user)

            # Handle "Remember Me" - extend session to 5 days
            if remember_me:
                request.session.set_expiry(5 * 24 * 60 * 60)  # 5 days in seconds
            else:
                request.session.set_expiry(0)  # Session expires when browser closes

            # Redirect based on user role - check SuperAdmin first
            from accounts.models import SuperAdmin

            if SuperAdmin.objects.filter(user=user, is_active=True).exists():
                messages.success(request, f"Welcome SuperAdmin {user.username}!")
                return redirect("super_admin_dashboard")

            # Then check if regular admin
            try:
                if user.profile.is_admin():
                    messages.success(request, f"Welcome back, {user.profile.name}!")
                    return redirect("admin_dashboard_overview")
                else:
                    messages.success(request, f"Welcome back, {user.profile.name}!")
                    return redirect("dashboard_home")
            except Profile.DoesNotExist:
                # User has no profile, send to dashboard
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("dashboard_home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "accounts/login.html")


def superadmin_login(request):
    """
    SuperAdmin-only login view
    Authenticates using username and password only (no email required)
    Exclusive to SuperAdmin users
    """
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.profile.is_superadmin():
            return redirect("super_admin_dashboard")
        return redirect("dashboard_home")

    if request.method == "POST":
        form = SuperAdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"].strip()

            # Check if superadmin exists in SuperAdmin table
            try:
                superadmin = SuperAdmin.objects.get(username=username, is_active=True)
            except SuperAdmin.DoesNotExist:
                messages.error(request, "Invalid username or password.")
                return render(request, "accounts/superadmin_login.html", {"form": form})

            # Verify password using Django's password hasher
            if check_password(password, superadmin.password_hash):
                # If linked to user account, login that user
                if superadmin.user:
                    # Specify backend explicitly for multiple auth backends
                    login(
                        request,
                        superadmin.user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    messages.success(
                        request,
                        f"Welcome Super Admin, {superadmin.username}!",
                    )
                    return redirect("super_admin_dashboard")
                else:
                    messages.error(
                        request,
                        "SuperAdmin account is not properly linked to user account.",
                    )
                    return render(
                        request, "accounts/superadmin_login.html", {"form": form}
                    )
            else:
                messages.error(request, "Invalid username or password.")
                return render(request, "accounts/superadmin_login.html", {"form": form})
        else:
            messages.error(request, "Please provide both username and password.")
            return render(request, "accounts/superadmin_login.html", {"form": form})
    else:
        form = SuperAdminLoginForm()

    return render(request, "accounts/superadmin_login.html", {"form": form})


def verify_email(request):
    """Handle verification code submission and activate user profile."""
    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"].strip()
            code = form.cleaned_data["code"].strip()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "No account found for that email.")
                return redirect("register")

            # Find latest non-expired verification for this user
            verification_qs = EmailVerification.objects.filter(
                user=user, code=code, expires_at__gt=timezone.now()
            )
            if verification_qs.exists():
                # Mark profile verified
                profile, _ = Profile.objects.get_or_create(user=user)
                profile.is_verified = True
                profile.save()
                # Optionally delete verification records
                EmailVerification.objects.filter(user=user).delete()
                messages.success(
                    request, "Email verified successfully. You can now log in."
                )
                return redirect("login")
            else:
                messages.error(request, "Invalid or expired verification code.")
    else:
        form = EmailVerificationForm()

    return render(request, "accounts/verify_email.html", {"form": form})


def resend_verification(request):
    """Resend a verification code to the provided email."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found for that email.")
            return redirect("register")

        code = EmailVerification.generate_code()
        expires = timezone.now() + timedelta(hours=24)
        EmailVerification.objects.create(user=user, code=code, expires_at=expires)
        try:
            send_mail(
                "CampusFix Email Verification",
                f"Your CampusFix verification code is: {code}",
                getattr(settings, "DEFAULT_FROM_EMAIL", None),
                [user.email],
                fail_silently=False,
            )
        except Exception:
            pass
        messages.success(request, "Verification code resent. Check your email.")
        return redirect("verify_email")


@login_required(login_url="login")
def logout_view(request):
    """
    User logout view
    Logs out user and redirects to login page
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def password_reset_request(request):
    """
    First step of password reset: User enters email and receives code
    """
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                # Generate reset code
                code = PasswordResetCode.generate_code()
                expires = timezone.now() + timedelta(hours=1)
                PasswordResetCode.objects.create(
                    user=user, code=code, expires_at=expires
                )
                # Send code via email (not link)
                send_password_reset_email(user.email, code)
                messages.success(
                    request,
                    "A password reset code has been sent to your email. Please check your inbox.",
                )
                return redirect(f"/accounts/password_reset/code/?email={email}")
            except User.DoesNotExist:
                messages.error(request, "No account found with this email address.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = PasswordResetForm()

    return render(request, "accounts/password_reset.html", {"form": form})


def password_reset_code(request):
    """
    Second step of password reset: User enters code and new password
    """
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    # Get email from either GET parameter or POST data
    email = request.GET.get("email", "") or request.POST.get("email", "")

    if request.method == "POST":
        form = PasswordResetCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email", "").strip()
            code = form.cleaned_data["code"].strip()
            new_password = form.cleaned_data["new_password1"]

            try:
                user = User.objects.get(email=email)
                reset_code_obj = PasswordResetCode.objects.get(
                    user=user, code=code, expires_at__gt=timezone.now()
                )
                # Code is valid, set new password
                user.set_password(new_password)
                user.save()

                # Consume the reset code
                reset_code_obj.delete()

                messages.success(
                    request,
                    "Your password has been reset successfully! You can now login.",
                )
                return redirect("login")
            except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
                messages.error(request, "Invalid or expired reset code.")
                form.add_error("code", "Invalid or expired reset code.")
    else:
        form = PasswordResetCodeForm()

    return render(
        request, "accounts/password_reset_code.html", {"form": form, "email": email}
    )


class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    """
    View shown after password reset is complete
    """

    template_name = "accounts/password_reset_complete.html"


@login_required(login_url="login")
def login_redirect(request):
    """Redirect users to their respective dashboards based on role."""
    try:
        profile = request.user.profile
        if profile.role == "superadmin":
            return redirect("super_admin_dashboard")
        elif profile.role == "admin":
            return redirect("admin_dashboard_overview")
        return redirect("dashboard_home")
    except Profile.DoesNotExist:
        # Priority fallback: Check if user is in SuperAdmin table
        from accounts.models import SuperAdmin

        if SuperAdmin.objects.filter(user=request.user, is_active=True).exists():
            return redirect("super_admin_dashboard")

        # Superuser fallback
        if request.user.is_superuser:
            return redirect("super_admin_dashboard")
        return redirect("dashboard_home")


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def contact_messages_list(request):
    """List incoming contact messages for staff/admins."""
    # Support filtering: all (default), unread, new
    filter_mode = request.GET.get("filter", "all")
    messages_qs = ContactMessage.objects.all()

    if filter_mode == "unread":
        messages_qs = messages_qs.filter(is_read=False)
    elif filter_mode == "new":
        from datetime import timedelta

        cutoff = timezone.now() - timedelta(days=7)
        messages_qs = messages_qs.filter(created_at__gte=cutoff)

    messages_qs = messages_qs.order_by("-created_at")
    return render(
        request, "accounts/contact_messages_list.html", {"messages": messages_qs}
    )


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def contact_reply(request, pk):
    contact = ContactMessage.objects.filter(pk=pk).first()
    if not contact:
        messages.error(request, "Contact message not found.")
        return redirect("contact_messages_list")

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data["reply_text"]
            # send reply email
            subject = f"Re: {contact.subject}"
            ok = send_reply_email(contact.email, subject, reply_text)

            # persist reply record
            try:
                ContactReply.objects.create(
                    message=contact,
                    replier=request.user,
                    reply_text=reply_text,
                    sent_to=contact.email,
                )
                contact.is_replied = True
                contact.is_read = True
                contact.save()
            except Exception:
                pass

            if ok:
                messages.success(request, "Reply sent and saved.")
            else:
                messages.error(
                    request, "Failed to send reply email, but saved locally."
                )
            return redirect("contact_messages_list")
    else:
        form = ReplyForm()

    return render(
        request, "accounts/contact_reply.html", {"contact": contact, "form": form}
    )


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def contact_soft_delete(request, pk):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("contact_messages_list")

    contact = ContactMessage.objects.filter(pk=pk).first()
    if not contact:
        messages.error(request, "Contact message not found.")
        return redirect("contact_messages_list")
    contact.is_deleted = True
    contact.deleted_by = request.user
    contact.deleted_at = timezone.now()
    contact.save()
    messages.success(request, "Message soft-deleted.")
    return redirect("contact_messages_list")


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser)
def contact_hard_delete(request, pk):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("contact_messages_list")

    contact = ContactMessage.objects.filter(pk=pk).first()
    if not contact:
        messages.error(request, "Contact message not found.")
        return redirect("contact_messages_list")
    contact.delete()
    messages.success(request, "Message permanently deleted.")
    return redirect("contact_messages_list")


@login_required(login_url="login")
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def contact_view(request, pk):
    """View-only page for a contact message. Marks message as read."""
    contact = ContactMessage.objects.filter(pk=pk).first()
    if not contact:
        messages.error(request, "Contact message not found.")
        return redirect("contact_messages_list")

    # mark read
    if not contact.is_read:
        contact.is_read = True
        try:
            contact.save()
        except Exception:
            pass

    return render(request, "accounts/contact_view.html", {"contact": contact})

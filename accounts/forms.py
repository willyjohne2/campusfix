from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm as DjangoPasswordResetForm,
)
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    """
    User registration form - extends Django's UserCreationForm
    Fields: name, email, password1, password2
    """

    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your full name", "class": "form-control"}
        ),
        label="Full Name",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email address", "class": "form-control"}
        ),
        label="Email Address",
    )

    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]

    def clean_email(self):
        """Validate that email is not already registered"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "This email is already registered. Please use a different email."
            )
        return email

    def save(self, commit=True):
        """
        Save user with email as username
        """
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Use email as username
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Custom login form - fields: email and password
    """

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email address",
                "class": "form-control",
                "autofocus": True,
            }
        ),
        label="Email Address",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-control"}
        ),
        label="Password",
    )

    def clean_username(self):
        """
        Override to authenticate with email instead of username
        """
        email = self.cleaned_data.get("username")
        return email


class PasswordResetForm(DjangoPasswordResetForm):
    """
    Custom password reset form extending Django's PasswordResetForm
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your registered email address",
                "class": "form-control",
            }
        ),
        label="Email Address",
    )

    def clean_email(self):
        """Validate that email exists in the system"""
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}), label="Email"
    )
    code = forms.CharField(
        max_length=8,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter verification code"}
        ),
        label="Verification Code",
    )


class PasswordResetCodeForm(forms.Form):
    """
    Form for resetting password with code, new password, and confirmation
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label="Email Address",
        required=True,
    )
    code = forms.CharField(
        max_length=8,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter the code sent to your email",
            }
        ),
        label="Reset Code",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        ),
        label="New Password",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        ),
        label="Confirm Password",
    )

    def clean(self):
        """Validate that passwords match"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match.")
        return cleaned_data


class ContactForm(forms.Form):
    """Simple contact form for site visitors"""

    name = forms.CharField(
        max_length=120,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your name"}
        ),
        label="Your name",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your email"}
        ),
        label="Your email",
    )
    subject = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
        label="Subject",
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 6, "placeholder": "Your message"}
        ),
        label="Message",
    )


class ReplyForm(forms.Form):
    """Form for admins to reply to contact messages"""

    reply_text = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 6, "placeholder": "Reply text"}
        ),
        label="Reply",
    )

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string
from django.conf import settings


class Profile(models.Model):
    """
    Extended user profile model to store additional user information
    aligned with registration form fields (name, email)
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=150)  # Display name from registration form
    is_verified = models.BooleanField(default=False)  # Email verification status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the display name or fallback to email"""
        return self.name if self.name else self.user.email

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["-created_at"]


class EmailVerification(models.Model):
    """Stores email verification codes for users."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="email_verifications"
    )
    code = models.CharField(max_length=8, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Verification for {self.user.email} - {self.code}"

    @staticmethod
    def generate_code(length=6):
        return "".join(random.choices(string.digits, k=length))

    def is_expired(self):
        return timezone.now() > self.expires_at


class PasswordResetCode(models.Model):
    """Stores one-time codes for password reset verification."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="password_reset_codes"
    )
    code = models.CharField(max_length=12, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Password reset for {self.user.email} - {self.code}"

    @staticmethod
    def generate_code(length=8):
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choices(chars, k=length))

    def is_expired(self):
        return timezone.now() > self.expires_at


class ContactMessage(models.Model):
    """Stores messages submitted via the contact form."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)
    # read state for admin inbox
    is_read = models.BooleanField(default=False)
    # soft-delete fields
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="deleted_contact_messages",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Contact from {self.name} <{self.email}> - {self.subject}"


class ContactReply(models.Model):
    """A reply sent by an admin in response to a ContactMessage."""

    message = models.ForeignKey(
        ContactMessage, on_delete=models.CASCADE, related_name="replies"
    )
    replier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.EmailField()  # copy of recipient email at time of sending
    # mark reply as deleted (soft) if needed
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="deleted_contact_replies",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        who = self.replier.get_full_name() if self.replier else "(deleted user)"
        return f"Reply to {self.message.email} by {who}"

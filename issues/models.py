from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid
import hashlib


class Issue(models.Model):
    """
    Model for campus issues reported by users
    """

    CATEGORY_CHOICES = [
        ("Maintenance", "Maintenance"),
        ("IT", "IT"),
        ("Facilities", "Facilities"),
        ("Cleanliness", "Cleanliness"),
        ("Security", "Security"),
        ("Other", "Other"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Rejected", "Rejected"),
    ]

    # Core fields
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="Other"
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="Medium"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    # User reference
    reported_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reported_issues"
    )

    # Anonymous code - unique per post for anonymity
    anonymous_code = models.CharField(
        max_length=12, unique=True, db_index=True, null=True, blank=True
    )

    # Attachment
    attachment = models.ImageField(
        upload_to="issues/attachments/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Admin notes
    admin_notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["category", "status"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def is_urgent(self):
        """Check if issue is urgent (High or Critical priority)"""
        return self.priority in ["High", "Critical"]

    def generate_anonymous_code(self):
        """Generate a unique anonymous code for this post"""
        if not self.anonymous_code:
            # Create unique code from UUID and timestamp
            unique_string = f"{uuid.uuid4()}{timezone.now().timestamp()}"
            # Hash it and take first 12 characters
            code = hashlib.md5(unique_string.encode()).hexdigest()[:12].upper()
            self.anonymous_code = code
        return self.anonymous_code

    def save(self, *args, **kwargs):
        """Generate anonymous code before saving"""
        if not self.anonymous_code:
            self.generate_anonymous_code()
        super().save(*args, **kwargs)

    def get_display_name(self, user=None):
        """
        Get the name to display for the reporter
        - For superadmins: show real name + code
        - For others: show only anonymous code
        """
        if user and (user.is_superuser or user.is_staff):
            return f"{self.reported_by.get_full_name() or self.reported_by.username} ({self.anonymous_code})"
        return f"Posted by {self.anonymous_code}"


class IssueComment(models.Model):
    """
    Model for comments on issues
    """

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="issue_comments"
    )
    content = models.TextField(blank=False)
    is_admin_response = models.BooleanField(
        default=False
    )  # Mark if this is an official admin response
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.issue.title}"

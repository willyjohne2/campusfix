from django import forms
from django.core.exceptions import ValidationError
from .models import Issue, IssueComment


class ReportIssueForm(forms.ModelForm):
    """
    Form for reporting a new issue
    Validates all required fields and file attachments
    """

    class Meta:
        model = Issue
        fields = ["title", "category", "description", "priority", "attachment"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter issue title",
                    "class": "form-control",
                    "maxlength": 200,
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the issue in detail",
                    "class": "form-control",
                    "rows": 5,
                }
            ),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "attachment": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }
        labels = {
            "title": "Issue Title",
            "category": "Category",
            "description": "Description",
            "priority": "Priority Level",
            "attachment": "Attachment (Optional)",
        }

    def clean_title(self):
        """Validate title - minimum 3 characters"""
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters long.")
        return title

    def clean_description(self):
        """Validate description - minimum 5 characters"""
        description = self.cleaned_data.get("description", "").strip()
        if len(description) < 5:
            raise ValidationError("Description must be at least 5 characters long.")
        return description

    def clean_attachment(self):
        """Validate attachment file"""
        attachment = self.cleaned_data.get("attachment")

        if attachment:
            # Check file size (max 5MB)
            if attachment.size > 5 * 1024 * 1024:
                raise ValidationError("File size must not exceed 5MB.")

            # Check file type
            allowed_extensions = ["jpg", "jpeg", "png", "gif"]
            file_extension = attachment.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError("Only image files (JPG, PNG, GIF) are allowed.")

        return attachment


class UpdateIssueStatusForm(forms.ModelForm):
    """
    Form for admins to update issue status
    """

    class Meta:
        model = Issue
        fields = ["status", "admin_notes", "assigned_to"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "admin_notes": forms.Textarea(
                attrs={
                    "placeholder": "Add notes about this issue",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "status": "Status",
            "admin_notes": "Admin Notes",
            "assigned_to": "Assign To",
        }


class IssueCommentForm(forms.ModelForm):
    """
    Form for adding comments to issues
    """

    class Meta:
        model = IssueComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Add a comment...",
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }
        labels = {
            "content": "Comment",
        }

    def clean_content(self):
        """Validate comment content"""
        content = self.cleaned_data.get("content", "").strip()
        if len(content) < 2:
            raise ValidationError("Comment must be at least 2 characters long.")
        if len(content) > 1000:
            raise ValidationError("Comment must not exceed 1000 characters.")
        return content


class IssueFilterForm(forms.Form):
    """
    Form for filtering issues
    """

    FILTER_CHOICES = [
        ("", "All Statuses"),
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Rejected", "Rejected"),
    ]

    CATEGORY_FILTER_CHOICES = [
        ("", "All Categories"),
        ("Maintenance", "Maintenance"),
        ("IT", "IT"),
        ("Facilities", "Facilities"),
        ("Cleanliness", "Cleanliness"),
        ("Security", "Security"),
        ("Other", "Other"),
    ]

    status = forms.ChoiceField(
        choices=FILTER_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    category = forms.ChoiceField(
        choices=CATEGORY_FILTER_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Search issues...", "class": "form-control"}
        ),
    )

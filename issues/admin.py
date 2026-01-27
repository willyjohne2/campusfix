from django.contrib import admin
from .models import Issue, IssueComment


class IssueCommentInline(admin.TabularInline):
    model = IssueComment
    extra = 0
    readonly_fields = ("author", "created_at", "updated_at")
    fields = ("author", "content", "is_admin_response", "created_at")


@admin.action(description="Mark selected issues as Resolved")
def mark_resolved(modeladmin, request, queryset):
    queryset.update(status="Resolved")


@admin.action(description="Assign selected issues to current admin")
def assign_to_self(modeladmin, request, queryset):
    queryset.update(assigned_to=request.user)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "priority",
        "status",
        "reported_by",
        "assigned_to",
        "created_at",
    ]
    list_filter = ["status", "category", "priority", "created_at", "assigned_to"]
    search_fields = ["title", "description", "reported_by__email"]
    readonly_fields = ["created_at", "updated_at", "reported_by", "anonymous_code"]
    inlines = [IssueCommentInline]
    actions = [mark_resolved, assign_to_self]
    list_select_related = ("reported_by", "assigned_to")

    fieldsets = (
        (
            "Issue Information",
            {"fields": ("title", "description", "category", "priority")},
        ),
        ("Status & Assignment", {"fields": ("status", "assigned_to", "admin_notes")}),
        ("Reporter", {"fields": ("reported_by", "anonymous_code")}),
        ("Attachment", {"fields": ("attachment",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ["author", "issue", "is_admin_response", "created_at"]
    list_filter = ["created_at", "issue", "is_admin_response"]
    search_fields = ["content", "author__email", "issue__title"]
    readonly_fields = ["created_at", "updated_at", "author"]

    fieldsets = (
        (
            "Comment Information",
            {"fields": ("issue", "author", "content", "is_admin_response")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

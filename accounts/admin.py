from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Profile
from .models import ContactMessage, ContactReply


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "is_verified", "created_at"]
    list_filter = ["is_verified", "created_at"]
    search_fields = ["name", "user__email"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("User Information", {"fields": ("user", "name")}),
        ("Verification", {"fields": ("is_verified",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def has_add_permission(self, request):
        return False


@admin.action(description="Deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="Activate selected users")
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="Make selected users staff (Admin)")
def make_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)


@admin.action(description="Revoke staff status for selected users")
def remove_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)


class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
        "last_login",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")
    actions = [deactivate_users, activate_users, make_staff, remove_staff]


# Unregister the default User admin and register our customized one
try:
    admin.site.unregister(User)
except Exception:
    pass

admin.site.register(User, UserAdmin)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "email",
        "subject",
        "is_replied",
        "is_read",
        "is_deleted",
        "created_at",
    ]
    search_fields = ["name", "email", "subject", "message"]
    list_filter = ["is_replied", "is_deleted", "created_at"]
    actions = ["soft_delete_messages", "restore_messages", "hard_delete_messages"]

    @admin.action(description="Soft delete selected messages")
    def soft_delete_messages(self, request, queryset):
        queryset.update(is_deleted=True, deleted_by=request.user)

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    @admin.action(description="Restore selected messages")
    def restore_messages(self, request, queryset):
        queryset.update(is_deleted=False, deleted_by=None)

    @admin.action(description="Hard delete selected messages (superusers only)")
    def hard_delete_messages(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can hard-delete messages.")
            return
        queryset.delete()

    # add read/unread actions
    actions += ["mark_as_read", "mark_as_unread"]


@admin.register(ContactReply)
class ContactReplyAdmin(admin.ModelAdmin):
    list_display = ["message", "replier", "sent_to", "is_deleted", "created_at"]
    search_fields = ["reply_text", "sent_to"]
    readonly_fields = ["created_at"]
    actions = ["soft_delete_replies", "restore_replies", "hard_delete_replies"]

    @admin.action(description="Soft delete selected replies")
    def soft_delete_replies(self, request, queryset):
        queryset.update(is_deleted=True, deleted_by=request.user)

    @admin.action(description="Restore selected replies")
    def restore_replies(self, request, queryset):
        queryset.update(is_deleted=False, deleted_by=None)

    @admin.action(description="Hard delete selected replies (superusers only)")
    def hard_delete_replies(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can hard-delete replies.")
            return
        queryset.delete()

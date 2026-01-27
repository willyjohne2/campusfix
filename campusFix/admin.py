from django.contrib import admin


class SuperUserOnlyAdminSite(admin.AdminSite):
    """Admin site that only allows access to superusers."""

    def has_permission(self, request):
        """Only allow active superusers to access the admin site."""
        return bool(
            request.user and request.user.is_active and request.user.is_superuser
        )


# Replace the default admin site with our superuser-only site
admin.site = SuperUserOnlyAdminSite()
admin.site.site_header = "CampusFix — Super Admin"
admin.site.site_title = "CampusFix Super Admin"
admin.site.index_title = "CampusFix System Administration"
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import Count
from issues.models import Issue


# Custom User Admin
@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_superuser", "date_joined")
    list_filter = ("is_staff", "is_superuser", "date_joined")
    actions = ["make_admin", "make_super_admin"]

    def make_admin(self, request, queryset):
        admin_group, created = Group.objects.get_or_create(name="Admins")
        for user in queryset:
            user.groups.add(admin_group)
            user.is_staff = True
            user.save()
        self.message_user(request, "Selected users have been made admins.")

    make_admin.short_description = "Make selected users Admins"

    def make_super_admin(self, request, queryset):
        for user in queryset:
            user.is_superuser = True
            user.is_staff = True
            user.save()
        self.message_user(request, "Selected users have been made super admins.")

    make_super_admin.short_description = "Make selected users Super Admins"


# Custom Issue Admin
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "priority", "date_reported")
    list_filter = ("status", "category", "priority")
    actions = ["mark_as_in_progress", "mark_as_fixed"]

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status="In Progress")
        self.message_user(request, "Selected issues have been marked as In Progress.")

    mark_as_in_progress.short_description = "Mark selected issues as In Progress"

    def mark_as_fixed(self, request, queryset):
        queryset.update(status="Fixed")
        self.message_user(request, "Selected issues have been marked as Fixed.")

    mark_as_fixed.short_description = "Mark selected issues as Fixed"


# Add a dashboard overview for super admins
class SuperAdminDashboard(admin.AdminSite):
    site_header = "Super Admin Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["total_users"] = User.objects.count()
        extra_context["failed_logins"] = 0  # Placeholder, requires custom tracking
        extra_context["total_issues"] = Issue.objects.count()
        extra_context["issues_by_status"] = Issue.objects.values("status").annotate(
            count=Count("status")
        )
        return super().index(request, extra_context=extra_context)


super_admin_site = SuperAdminDashboard(name="super_admin")

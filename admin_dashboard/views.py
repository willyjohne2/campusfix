from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncWeek, TruncDay
from datetime import timedelta
from issues.models import Issue, IssueComment
from accounts.models import ContactMessage, Profile, SuperAdmin
from .models import AdminActivity
from django.contrib.auth.hashers import make_password


# Helper function to check if user is an admin
def is_admin(user):
    """Check if user has admin role"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.is_admin()
    except:
        return False


@user_passes_test(is_admin)
def dashboard_overview(request):
    """Admin dashboard overview with key metrics and analytics"""

    # Basic stats
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status="Pending").count()
    in_progress_issues = Issue.objects.filter(status="In Progress").count()
    resolved_issues = Issue.objects.filter(status="Resolved").count()
    rejected_issues = Issue.objects.filter(status="Rejected").count()

    # Weekly registration data (last 8 weeks)
    eight_weeks_ago = timezone.now() - timedelta(weeks=8)
    weekly_registrations = (
        User.objects.filter(date_joined__gte=eight_weeks_ago)
        .annotate(week=TruncWeek("date_joined"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )

    # Weekly issues data (last 8 weeks)
    weekly_issues = (
        Issue.objects.filter(created_at__gte=eight_weeks_ago)
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )

    # Daily stats for last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_issues = (
        Issue.objects.filter(created_at__gte=seven_days_ago)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # Top 5 admins by resolved issues (only show if superadmin)
    top_admins = None
    if request.user.profile.is_superadmin():
        # Get all resolved issues with admin activity
        admin_resolutions = (
            AdminActivity.objects.filter(action__icontains="Resolved")
            .values("admin__profile__name", "admin__id")
            .annotate(resolved_count=Count("id"))
            .order_by("-resolved_count")[:5]
        )
        top_admins = list(admin_resolutions)

    # Top 5 users by reported issues (only show if superadmin)
    top_reporters = None
    if request.user.profile.is_superadmin():
        top_reporters = (
            Issue.objects.values("reported_by__profile__name", "reported_by__id")
            .annotate(issue_count=Count("id"))
            .order_by("-issue_count")[:5]
        )
        top_reporters = list(top_reporters)

    # Recent issues
    recent_issues = Issue.objects.all().order_by("-created_at")[:5]

    # Recent admin activity
    recent_activity = AdminActivity.objects.filter(admin=request.user).order_by(
        "-timestamp"
    )[:5]

    context = {
        "total_issues": total_issues,
        "pending_issues": pending_issues,
        "in_progress_issues": in_progress_issues,
        "resolved_issues": resolved_issues,
        "rejected_issues": rejected_issues,
        "recent_issues": recent_issues,
        "recent_activity": recent_activity,
        "recent_messages": ContactMessage.objects.filter(is_deleted=False).order_by(
            "-created_at"
        )[:6],
        # Analytics data for charts
        "weekly_registrations": list(weekly_registrations),
        "weekly_issues": list(weekly_issues),
        "daily_issues": list(daily_issues),
        "top_admins": top_admins,
        "top_reporters": top_reporters,
        # Total users
        "total_users": User.objects.count(),
    }
    return render(request, "admin_dashboard/overview.html", context)


@user_passes_test(is_admin)
def issue_list(request):
    """List all issues with filtering options"""
    status_filter = request.GET.get("status")
    category_filter = request.GET.get("category")
    priority_filter = request.GET.get("priority")
    search_query = request.GET.get("search")

    issues = Issue.objects.all().order_by("-created_at")

    if status_filter:
        issues = issues.filter(status=status_filter)
    if category_filter:
        issues = issues.filter(category=category_filter)
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    if search_query:
        issues = issues.filter(title__icontains=search_query) | issues.filter(
            description__icontains=search_query
        )

    # Pagination - 10 issues per page
    paginator = Paginator(issues, 10)
    page_number = request.GET.get("page")
    issues_page = paginator.get_page(page_number)

    # Get unique categories and priorities for filters
    categories = Issue.objects.values_list("category", flat=True).distinct()
    priorities = Issue.objects.values_list("priority", flat=True).distinct()

    context = {
        "issues": issues_page,
        "status_filter": status_filter,
        "category_filter": category_filter,
        "priority_filter": priority_filter,
        "search_query": search_query,
        "categories": categories,
        "priorities": priorities,
        "total_count": issues.count(),
    }
    return render(request, "admin_dashboard/issue_list.html", context)


@user_passes_test(is_admin)
def issue_detail(request, issue_id):
    """View issue details and manage status/comments"""
    issue = get_object_or_404(Issue, id=issue_id)
    comments = IssueComment.objects.filter(issue=issue).order_by("-created_at")

    if request.method == "POST":
        action = request.POST.get("action")

        # Update issue status
        if action == "update_status":
            new_status = request.POST.get("status")
            if new_status:
                issue.status = new_status
                issue.save()

                # Log admin activity
                AdminActivity.objects.create(
                    admin=request.user,
                    issue=issue,
                    action=f"Updated status to {new_status}",
                )
                messages.success(request, f"Issue status updated to {new_status}.")

        # Add admin response
        elif action == "add_response":
            comment_text = request.POST.get("comment")
            if comment_text:
                IssueComment.objects.create(
                    issue=issue,
                    author=request.user,
                    content=comment_text,
                    is_admin_response=True,
                )

                # Log admin activity
                AdminActivity.objects.create(
                    admin=request.user, issue=issue, action="Added official response"
                )
                messages.success(request, "Response added successfully.")

        return redirect("admin_issue_detail", issue_id=issue_id)

    context = {
        "issue": issue,
        "comments": comments,
        "reporter_name": issue.reported_by.first_name or issue.reported_by.username,
    }
    return render(request, "admin_dashboard/issue_detail.html", context)


@user_passes_test(is_admin)
def activity_log(request):
    """View admin activity logs"""
    activities = AdminActivity.objects.all().order_by("-timestamp")

    # Pagination - 20 activities per page
    paginator = Paginator(activities, 20)
    page_number = request.GET.get("page")
    activities_page = paginator.get_page(page_number)

    context = {
        "activities": activities_page,
    }
    return render(request, "admin_dashboard/activity_log.html", context)


# Helper function to check if user is superadmin
def is_superadmin(user):
    """Check if user has superadmin role"""
    if not user.is_authenticated:
        return False
    try:
        return user.profile.is_superadmin()
    except:
        return False


@user_passes_test(is_superadmin)
def super_admin_dashboard(request):
    """Super Admin Dashboard with comprehensive analytics and user management"""

    # Basic stats
    total_users = User.objects.count()
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status="Pending").count()
    in_progress_issues = Issue.objects.filter(status="In Progress").count()
    resolved_issues = Issue.objects.filter(status="Resolved").count()
    rejected_issues = Issue.objects.filter(status="Rejected").count()

    # User statistics by role
    user_count = Profile.objects.filter(role="user").count()
    admin_count = Profile.objects.filter(role="admin").count()
    superadmin_count = Profile.objects.filter(role="superadmin").count()

    # Weekly registration data (last 8 weeks)
    eight_weeks_ago = timezone.now() - timedelta(weeks=8)
    weekly_registrations = (
        User.objects.filter(date_joined__gte=eight_weeks_ago)
        .annotate(week=TruncWeek("date_joined"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )

    # Weekly issues data (last 8 weeks)
    weekly_issues = (
        Issue.objects.filter(created_at__gte=eight_weeks_ago)
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(count=Count("id"))
        .order_by("week")
    )

    # Daily stats for last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_issues = (
        Issue.objects.filter(created_at__gte=seven_days_ago)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # Top 5 admins by resolved issues
    admin_resolutions = (
        AdminActivity.objects.filter(action__icontains="Resolved")
        .values("admin__profile__name", "admin__id")
        .annotate(resolved_count=Count("id"))
        .order_by("-resolved_count")[:5]
    )

    # Top 5 users by reported issues
    top_reporters = (
        Issue.objects.values("reported_by__profile__name", "reported_by__id")
        .annotate(issue_count=Count("id"))
        .order_by("-issue_count")[:5]
    )

    # All users with role and activity info
    all_users = User.objects.select_related("profile").order_by("-date_joined")[:50]

    # Recent activity logs
    recent_activity = AdminActivity.objects.all().order_by("-timestamp")[:20]

    # Failed login attempts (from django-axes if available)
    failed_logins = []
    try:
        from axes.models import AccessAttempt

        failed_logins = AccessAttempt.objects.order_by("-attempt_time")[:20]
    except:
        pass

    # Recent issues
    recent_issues = Issue.objects.all().order_by("-created_at")[:20]

    context = {
        # Stats
        "total_users": total_users,
        "total_issues": total_issues,
        "pending_issues": pending_issues,
        "in_progress_issues": in_progress_issues,
        "resolved_issues": resolved_issues,
        "rejected_issues": rejected_issues,
        "user_count": user_count,
        "admin_count": admin_count,
        "superadmin_count": superadmin_count,
        # Charts data
        "weekly_registrations": list(weekly_registrations),
        "weekly_issues": list(weekly_issues),
        "daily_issues": list(daily_issues),
        "top_admins": list(admin_resolutions),
        "top_reporters": list(top_reporters),
        # Tables data
        "all_users": all_users,
        "recent_activity": recent_activity,
        "failed_logins": failed_logins,
        "recent_issues": recent_issues,
    }

    return render(request, "admin_dashboard/super_admin.html", context)


@user_passes_test(is_superadmin)
def promote_user(request, user_id):
    """Promote/demote user role"""
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        new_role = request.POST.get("role")
        superadmin_username = request.POST.get("superadmin_username", "").strip()

        if new_role in ["user", "admin", "superadmin"]:
            user.profile.role = new_role
            user.profile.save()

            # If promoting to superadmin, create SuperAdmin record
            if new_role == "superadmin":
                if not superadmin_username:
                    messages.error(
                        request,
                        "Username is required when promoting to SuperAdmin.",
                    )
                    return redirect("super_admin_dashboard")

                # Check if username already exists
                if SuperAdmin.objects.filter(username=superadmin_username).exists():
                    messages.error(
                        request, f"Username '{superadmin_username}' is already taken."
                    )
                    return redirect("super_admin_dashboard")

                # Create SuperAdmin record with temporary password
                # Note: Password should be set by the new superadmin separately
                temp_password = make_password("ChangeMe123!")
                superadmin, created = SuperAdmin.objects.get_or_create(
                    username=superadmin_username,
                    defaults={
                        "user": user,
                        "password_hash": temp_password,
                        "is_active": True,
                    },
                )

                if created:
                    messages.success(
                        request,
                        f"{user.profile.name} promoted to SuperAdmin with username '{superadmin_username}'. They should change their password on first login.",
                    )
                else:
                    messages.error(
                        request,
                        f"SuperAdmin username '{superadmin_username}' already exists.",
                    )
            else:
                messages.success(
                    request, f"{user.profile.name} role updated to {new_role}."
                )
        else:
            messages.error(request, "Invalid role specified.")

    return redirect("super_admin_dashboard")


@user_passes_test(is_superadmin)
def deactivate_user(request, user_id):
    """Deactivate/activate user account"""
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"{user.profile.name} has been {status}.")

    return redirect("super_admin_dashboard")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from issues.models import Issue, IssueComment
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Profile


@login_required(login_url="login")
def dashboard_home(request):
    # Admins should use admin dashboard, not user dashboard
    try:
        user_role = request.user.profile.role
        if user_role == "admin":
            messages.info(request, "Admins use the Admin Dashboard.")
            return redirect("admin_dashboard_overview")
        elif user_role == "superadmin":
            messages.info(request, "Super Admins use the Super Admin Dashboard.")
            return redirect("super_admin_dashboard")
    except Profile.DoesNotExist:
        pass  # User has no profile, allow them to continue

    # Get user's stats
    user_issues = Issue.objects.filter(reported_by=request.user)
    user_comments = IssueComment.objects.filter(author=request.user)
    total_issues = user_issues.count()
    total_comments = user_comments.count()
    resolved_issues = user_issues.filter(status="Resolved").count()

    # Calculate user ranking
    all_users_ranked = (
        Issue.objects.values("reported_by")
        .annotate(issue_count=Count("id"))
        .order_by("-issue_count")
    )

    user_rank = None
    total_contributors = all_users_ranked.count()
    for index, user_stat in enumerate(all_users_ranked, start=1):
        if user_stat["reported_by"] == request.user.id:
            user_rank = index
            break

    # Determine badge
    badge = None
    badge_color = None
    if total_issues >= 10:
        badge = "🏆 Super Contributor"
        badge_color = "#fbbf24"
    elif total_issues >= 5:
        badge = "⭐ Active Contributor"
        badge_color = "#3b82f6"
    elif total_issues >= 1:
        badge = "📝 Contributor"
        badge_color = "#10b981"

    context = {
        "total_issues": total_issues,
        "total_comments": total_comments,
        "resolved_issues": resolved_issues,
        "user_rank": user_rank,
        "total_contributors": total_contributors,
        "badge": badge,
        "badge_color": badge_color,
    }
    return render(request, "user_dashboard/dashboard_home.html", context)


@login_required(login_url="login")
def my_issues(request):
    # Admins should use admin dashboard, not user dashboard
    try:
        user_role = request.user.profile.role
        if user_role == "admin":
            messages.info(request, "Admins use the Admin Dashboard.")
            return redirect("admin_dashboard_overview")
        elif user_role == "superadmin":
            return redirect("super_admin_dashboard")
    except Profile.DoesNotExist:
        pass  # User has no profile, allow them to continue

    # Get user's issues with pagination
    user_issues = Issue.objects.filter(reported_by=request.user).order_by("-created_at")

    # Pagination - 10 issues per page
    paginator = Paginator(user_issues, 10)
    page_number = request.GET.get("page")
    issues_page = paginator.get_page(page_number)

    context = {
        "issues": issues_page,
        "total_count": user_issues.count(),
    }
    return render(request, "user_dashboard/my_issues.html", context)


# @login_required
def update_profile(request):
    return render(request, "user_dashboard/update_profile.html")


# @login_required
def change_password(request):
    return render(request, "user_dashboard/change_password.html")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from issues.models import Issue, IssueComment
from django.core.paginator import Paginator
from django.db.models import Q


@login_required(login_url="login")
def dashboard_home(request):
    # Get user's stats
    user_issues = Issue.objects.filter(reported_by=request.user)
    user_comments = IssueComment.objects.filter(author=request.user)
    total_issues = user_issues.count()
    total_comments = user_comments.count()
    resolved_issues = user_issues.filter(status="Resolved").count()

    context = {
        "total_issues": total_issues,
        "total_comments": total_comments,
        "resolved_issues": resolved_issues,
    }
    return render(request, "user_dashboard/dashboard_home.html", context)


@login_required(login_url="login")
def my_issues(request):
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

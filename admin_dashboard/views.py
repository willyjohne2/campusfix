from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from issues.models import Issue, IssueComment
from accounts.models import ContactMessage
from .models import AdminActivity


# Helper function to check if user is an admin
def is_admin(user):
    try:
        admin_group = Group.objects.get(name="Admins")
        return admin_group in user.groups.all()
    except Group.DoesNotExist:
        return False


@user_passes_test(is_admin)
def dashboard_overview(request):
    """Admin dashboard overview with key metrics"""
    total_issues = Issue.objects.count()
    pending_issues = Issue.objects.filter(status="Pending").count()
    in_progress_issues = Issue.objects.filter(status="In Progress").count()
    resolved_issues = Issue.objects.filter(status="Resolved").count()

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
        "recent_issues": recent_issues,
        "recent_activity": recent_activity,
        # include recent contact messages for admins
        "recent_messages": ContactMessage.objects.filter(is_deleted=False).order_by(
            "-created_at"
        )[:6],
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

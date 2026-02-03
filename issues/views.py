from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Issue, IssueComment
from .forms import (
    ReportIssueForm,
    UpdateIssueStatusForm,
    IssueCommentForm,
    IssueFilterForm,
)


def is_user_admin(user):
    """Helper function to check if a user is admin or superadmin"""
    if not user.is_authenticated:
        return False

    # Check if superadmin
    try:
        from accounts.models import SuperAdmin

        if SuperAdmin.objects.filter(user=user, is_active=True).exists():
            return True
    except:
        pass

    # Check if profile admin
    try:
        if user.profile.is_admin():
            return True
    except:
        pass

    return False


@login_required(login_url="login")
def report_issue(request):
    """
    View for reporting a new issue
    Only regular users (not admins/superadmins) can report issues
    """
    # Check if user is an admin or superadmin
    is_promoted = False
    try:
        user_role = request.user.profile.role
        if (
            user_role in ["admin", "superadmin"]
            or request.user.is_staff
            or request.user.is_superuser
        ):
            is_promoted = True
    except AttributeError:
        if request.user.is_staff or request.user.is_superuser:
            is_promoted = True

    if is_promoted:
        messages.error(
            request, "Administrators cannot report issues. Only regular users can."
        )
        if request.user.is_superuser or (
            hasattr(request.user, "profile")
            and request.user.profile.role == "superadmin"
        ):
            return redirect("super_admin_dashboard")
        return redirect("admin_dashboard_overview")

    if request.method == "POST":
        form = ReportIssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.reported_by = request.user
            issue.save()
            messages.success(request, "Issue reported successfully!")
            return redirect("issue_detail", issue_id=issue.id)
        else:
            # Display form errors
            if form.errors:
                print(f"Form errors: {form.errors}")  # Debug output
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ReportIssueForm()

    return render(request, "issues/report_issue.html", {"form": form})


@login_required(login_url="login")
def issue_list(request):
    """
    View to display list of issues with filtering and pagination
    """
    issues = Issue.objects.all()

    # Apply filters
    filter_form = IssueFilterForm(request.GET)
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get("status")
        category = filter_form.cleaned_data.get("category")
        search = filter_form.cleaned_data.get("search")

        if status:
            issues = issues.filter(status=status)
        if category:
            issues = issues.filter(category=category)
        if search:
            issues = issues.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

    # Pagination
    paginator = Paginator(issues, 10)  # 10 issues per page
    page_number = request.GET.get("page")
    issues_page = paginator.get_page(page_number)

    context = {
        "issues": issues_page,
        "filter_form": filter_form,
        "total_count": issues.count(),
    }

    return render(request, "issues/issue_list.html", context)


@login_required(login_url="login")
def my_issues(request):
    """
    View to display issues reported by the current user
    """
    issues = Issue.objects.filter(reported_by=request.user)

    # Apply filters
    filter_form = IssueFilterForm(request.GET)
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get("status")
        category = filter_form.cleaned_data.get("category")
        search = filter_form.cleaned_data.get("search")

        if status:
            issues = issues.filter(status=status)
        if category:
            issues = issues.filter(category=category)
        if search:
            issues = issues.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

    # Pagination
    paginator = Paginator(issues, 10)
    page_number = request.GET.get("page")
    issues_page = paginator.get_page(page_number)

    context = {
        "issues": issues_page,
        "filter_form": filter_form,
        "total_count": issues.count(),
        "my_issues": True,
    }

    return render(request, "issues/issue_list.html", context)


@login_required(login_url="login")
def issue_detail(request, issue_id):
    """
    View to display issue details and handle comments
    """
    issue = get_object_or_404(Issue, id=issue_id)

    # Handle comment submission
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect("login")

        # Check if user can comment (only issue owner or admin)
        can_comment = request.user == issue.reported_by or is_user_admin(request.user)

        if not can_comment:
            messages.error(
                request, "Only the issue owner, admins, and super admins can comment."
            )
            return redirect("issue_detail", issue_id=issue.id)

        # Handle both form submission and inline comment from homepage
        comment_text = request.POST.get("comment_text") or request.POST.get("content")

        if comment_text:
            comment = IssueComment(
                issue=issue, author=request.user, content=comment_text
            )
            comment.save()
            messages.success(request, "Comment added successfully!")
        else:
            form = IssueCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.issue = issue
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added successfully!")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        return redirect("issue_detail", issue_id=issue.id)
    else:
        form = IssueCommentForm()

    # Get all comments
    comments = IssueComment.objects.filter(issue=issue)

    can_admin_action = is_user_admin(request.user)

    context = {
        "issue": issue,
        "comments": comments,
        "form": form,
        "can_edit": request.user == issue.reported_by or can_admin_action,
        "can_comment": request.user == issue.reported_by or can_admin_action,
        "can_admin_action": can_admin_action,
    }

    return render(request, "issues/issue_detail.html", context)


@login_required(login_url="login")
def delete_issue(request, issue_id):
    """
    View to delete an issue (only by reporter or admin)
    """
    issue = get_object_or_404(Issue, id=issue_id)

    # Check permissions
    if request.user != issue.reported_by and not is_user_admin(request.user):
        messages.error(request, "You do not have permission to delete this issue.")
        return redirect("issue_detail", issue_id=issue.id)

    if request.method == "POST":
        issue.delete()
        messages.success(request, "Issue deleted successfully!")
        if is_user_admin(request.user):
            return redirect("issue_list")
        else:
            return redirect("my_issues")

    return render(request, "issues/issue_confirm_delete.html", {"issue": issue})


@login_required(login_url="login")
def update_issue_status(request, issue_id):
    """
    View for admins to update issue status
    Only accessible to admin users
    """
    issue = get_object_or_404(Issue, id=issue_id)

    # Check if user is admin
    if not is_user_admin(request.user):
        messages.error(request, "You do not have permission to update issue status.")
        return redirect("issue_detail", issue_id=issue.id)

    if request.method == "POST":
        form = UpdateIssueStatusForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, "Issue updated successfully!")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    return redirect("admin_issue_detail", issue_id=issue.id)

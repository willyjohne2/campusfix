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


@login_required(login_url="login")
def report_issue(request):
    """
    View for reporting a new issue
    Handles form submission with validation
    """
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

        # Check if user can comment (only issue owner, admin, or super admin)
        can_comment = (
            request.user == issue.reported_by
            or request.user.is_staff
            or request.user.is_superuser
        )

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

    context = {
        "issue": issue,
        "comments": comments,
        "form": form,
        "can_edit": request.user == issue.reported_by or request.user.is_staff,
        "can_comment": (
            request.user == issue.reported_by
            or request.user.is_staff
            or request.user.is_superuser
        ),
    }

    return render(request, "issues/issue_detail.html", context)


@login_required(login_url="login")
def delete_issue(request, issue_id):
    """
    View to delete an issue (only by reporter or admin)
    """
    issue = get_object_or_404(Issue, id=issue_id)

    # Check permissions
    if request.user != issue.reported_by and not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this issue.")
        return redirect("issue_detail", issue_id=issue.id)

    if request.method == "POST":
        issue.delete()
        messages.success(request, "Issue deleted successfully!")
        if request.user.is_staff:
            return redirect("issue_list")
        else:
            return redirect("my_issues")

    return render(request, "issues/issue_confirm_delete.html", {"issue": issue})


@login_required(login_url="login")
def update_issue_status(request, issue_id):
    """
    View for admins to update issue status
    Only accessible to staff/admin users
    """
    issue = get_object_or_404(Issue, id=issue_id)

    # Check if user is admin/staff
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to update issue status.")
        return redirect("issue_detail", issue_id=issue.id)

    if request.method == "POST":
        form = UpdateIssueStatusForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, "Issue updated successfully!")
            return redirect("issue_detail", issue_id=issue.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UpdateIssueStatusForm(instance=issue)

    context = {
        "issue": issue,
        "form": form,
    }

    return render(request, "issues/update_issue_status.html", context)

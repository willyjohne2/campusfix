from django.shortcuts import render
from django.http import HttpResponse
from issues.models import Issue
from django.db.models import Q
from django.contrib import messages
from accounts.forms import ContactForm
from accounts.email_utils import send_contact_email
from accounts.models import ContactMessage
from django.views.decorators.cache import never_cache

try:
    from django_ratelimit.decorators import ratelimit
except Exception:
    from django_ratelimit.decorators import ratelimit


@never_cache
def homepage(request):
    # If the user is an admin or superadmin, we use a slightly different content context
    # but the same statistics. In the template, we show/hide according to role.

    # Get category filter from GET parameters
    category_filter = request.GET.get("category", "")

    # Start with all issues
    issues_queryset = Issue.objects.all().select_related("reported_by")

    # Apply category filter if provided
    if category_filter:
        issues_queryset = issues_queryset.filter(category=category_filter)

    # Get recent issues ordered by creation date
    recent_issues = issues_queryset.order_by("-created_at")[:10]

    # Get platform statistics
    total_issues = Issue.objects.count()
    resolved_issues = Issue.objects.filter(status="Resolved").count()
    pending_issues = Issue.objects.filter(status="Pending").count()
    in_progress_issues = Issue.objects.filter(status="In Progress").count()

    # Use canonical category choices from the model to populate filter buttons
    all_categories = [choice[0] for choice in Issue.CATEGORY_CHOICES]

    context = {
        "recent_issues": recent_issues,
        "category_filter": category_filter,
        "all_categories": all_categories,
        "total_issues": total_issues,
        "resolved_issues": resolved_issues,
        "pending_issues": pending_issues,
        "in_progress_issues": in_progress_issues,
    }
    return render(request, "home.html", context)


def about_page(request):
    return render(request, "about.html")


def help_page(request):
    return render(request, "help.html")


def privacy_page(request):
    return render(request, "privacy.html")


@ratelimit(key="ip", rate="10/m", block=True)
def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # If user is authenticated, prefer their account details for name/email
            if request.user.is_authenticated:
                name = request.user.get_full_name() or request.user.username
                email = request.user.email
            else:
                name = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            # Persist the incoming contact message to the database
            try:
                ContactMessage.objects.create(
                    name=name, email=email, subject=subject, message=message
                )
            except Exception:
                # Don't fail the request if DB write has an issue
                pass

            ok = send_contact_email(name, email, subject, message)
            if ok:
                messages.success(
                    request, "Thanks — your message was sent. We'll reply soon."
                )
                form = ContactForm()
            else:
                messages.error(
                    request, "Sorry — we couldn't send your message right now."
                )
    else:
        # Prefill name/email and make them readonly for authenticated users
        if request.user.is_authenticated:
            name = request.user.get_full_name() or request.user.username
            email = request.user.email
            form = ContactForm(initial={"name": name, "email": email})
            # mark fields readonly in the widget attrs so users can't change them
            form.fields["name"].widget.attrs["readonly"] = True
            form.fields["email"].widget.attrs["readonly"] = True
        else:
            form = ContactForm()
    return render(request, "contact.html", {"form": form})

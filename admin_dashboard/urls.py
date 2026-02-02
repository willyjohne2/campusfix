from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_overview, name="admin_dashboard_overview"),
    path("issues/", views.issue_list, name="admin_issue_list"),
    path("issues/<int:issue_id>/", views.issue_detail, name="admin_issue_detail"),
    path("activity-log/", views.activity_log, name="admin_activity_log"),
    # Super Admin routes
    path("super-admin/", views.super_admin_dashboard, name="super_admin_dashboard"),
    path("super-admin/promote/<int:user_id>/", views.promote_user, name="promote_user"),
    path(
        "super-admin/deactivate/<int:user_id>/",
        views.deactivate_user,
        name="deactivate_user",
    ),
]

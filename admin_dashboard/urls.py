from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_overview, name="admin_dashboard_overview"),
    path("issues/", views.issue_list, name="admin_issue_list"),
    path("issues/<int:issue_id>/", views.issue_detail, name="admin_issue_detail"),
    path("activity-log/", views.activity_log, name="admin_activity_log"),
]

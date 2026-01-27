from django.urls import path
from . import views

urlpatterns = [
    path("", views.issue_list, name="issue_list"),
    path("report/", views.report_issue, name="report_issue"),
    path("my-issues/", views.my_issues, name="my_issues"),
    path("<int:issue_id>/", views.issue_detail, name="issue_detail"),
    path("<int:issue_id>/delete/", views.delete_issue, name="delete_issue"),
    path(
        "<int:issue_id>/update-status/",
        views.update_issue_status,
        name="update_issue_status",
    ),
]

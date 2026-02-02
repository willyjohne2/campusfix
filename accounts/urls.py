from django.urls import path
from . import views
from .views import login_redirect

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("superadmin-login/", views.superadmin_login, name="superadmin_login"),
    path("logout/", views.logout_view, name="logout"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("password_reset/code/", views.password_reset_code, name="password_reset_code"),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("redirect/", login_redirect, name="login_redirect"),
    path("verify/", views.verify_email, name="verify_email"),
    path("verify/resend/", views.resend_verification, name="resend_verification"),
    # Contact messages (staff/admin)
    path(
        "contact/messages/", views.contact_messages_list, name="contact_messages_list"
    ),
    path("contact/<int:pk>/reply/", views.contact_reply, name="contact_reply"),
    path(
        "contact/<int:pk>/soft-delete/",
        views.contact_soft_delete,
        name="contact_soft_delete",
    ),
    path(
        "contact/<int:pk>/hard-delete/",
        views.contact_hard_delete,
        name="contact_hard_delete",
    ),
    path("contact/<int:pk>/view/", views.contact_view, name="contact_view"),
]

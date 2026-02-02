"""
URL configuration for campusFix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import HttpResponse
from . import views


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/login/",
        "Disallow: /accounts/register/",
        "Disallow: /dashboard/",
        "Disallow: /media/",
        "",
        "Sitemap: {}/sitemap.xml".format(request.build_absolute_uri("/")[:-1]),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path("", views.homepage, name="home"),
    path("about/", views.about_page, name="about"),
    path("help/", views.help_page, name="help"),
    path("privacy/", views.privacy_page, name="privacy"),
    path("contact/", views.contact_page, name="contact"),
    path("dashboard/", include("user_dashboard.urls")),
    path("issues/", include("issues.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin-dashboard/", include("admin_dashboard.urls")),
    # SEO files
    path("robots.txt", robots_txt),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="application/xml"
        ),
    ),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

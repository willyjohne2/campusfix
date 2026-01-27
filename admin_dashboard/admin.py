from django.contrib import admin
from .models import AdminActivity


@admin.register(AdminActivity)
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ["admin", "action", "issue", "timestamp"]
    list_filter = ["admin", "timestamp"]
    search_fields = ["admin__username", "action", "issue__title"]
    readonly_fields = ["admin", "action", "issue", "timestamp"]

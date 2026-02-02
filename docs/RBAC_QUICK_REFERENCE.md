# Quick Reference: Role-Based Access Control

## Permission Matrix at a Glance

| Action                   |  User  | Admin  | SuperAdmin |
| ------------------------ | :----: | :----: | :--------: |
| **Report Issues**        |   ✅   |   ❌   |     ❌     |
| **Comment on Issues**    | ✅ Own | ✅ All |   ✅ All   |
| **Delete Issues**        | ✅ Own | ✅ All |   ✅ All   |
| **Update Issue Status**  |   ❌   |   ✅   |     ✅     |
| **View Reporter Name**   |   ❌   |   ✅   |     ✅     |
| **Soft Delete Messages** |   ❌   |   ✅   |     ✅     |
| **Hard Delete Messages** |   ❌   |   ❌   |     ✅     |
| **See Full Emails**      |   ❌   |   ❌   |     ✅     |

## Permission Check Cheat Sheet

### In Python Views

```python
# Check if admin (admin OR superadmin)
if request.user.profile.is_admin():
    # user is admin or superadmin

# Check if only superadmin
if request.user.profile.is_superadmin():
    # user is superadmin only

# Check if regular user
if request.user.profile.is_regular_user():
    # user is regular user
```

### In Django Templates

```django
{% if user.profile.is_admin %}
    <!-- visible to admins and superadmins -->
{% endif %}

{% if user.profile.is_superadmin %}
    <!-- visible to superadmins only -->
{% endif %}

{% if user.profile.is_regular_user %}
    <!-- visible to regular users only -->
{% endif %}
```

## Admin Panel Actions

### Assign Roles to Users

1. Go to Django Admin → Users
2. Select user(s)
3. Choose from dropdown:
   - "Assign User role to selected users"
   - "Assign Admin role to selected users"
   - "Assign SuperAdmin role to selected users"
4. Click "Go"

### View User Roles

- Django Admin → Users: Role column shows current role
- Django Admin → Profiles: Role is editable directly

## Database Schema

```sql
-- Profile table
ALTER TABLE accounts_profile ADD COLUMN role varchar(20);

-- Choices: 'user', 'admin', 'superadmin'
-- Default: 'user'
```

## Migration Commands

```bash
# First time setup
python manage.py migrate accounts

# Sync existing users from legacy is_staff/is_superuser
python manage.py sync_user_roles

# Preview changes before applying
python manage.py sync_user_roles --dry-run
```

## Common Scenarios

### Issue Reporter Trying to Access Admin Dashboard

```
❌ Blocked by: @user_passes_test(is_admin)
```

### Admin Trying to Report an Issue

```
❌ Blocked by: if request.user.profile.is_admin(): error & redirect
```

### SuperAdmin Hard-Deleting a Message

```
✅ Allowed by: if request.user.profile.is_superadmin()
```

### Regular User Trying to Hard-Delete

```
❌ Blocked by: if not request.user.profile.is_superadmin(): error & return
```

## Files to Know

| File                                              | Purpose                                 |
| ------------------------------------------------- | --------------------------------------- |
| `accounts/models.py`                              | Profile model with role field & helpers |
| `accounts/admin.py`                               | Admin panel role management             |
| `admin_dashboard/views.py`                        | Admin dashboard access control          |
| `issues/views.py`                                 | Issue management with role checks       |
| `accounts/management/commands/sync_user_roles.py` | Legacy data migration                   |
| `ROLE_BASED_ACCESS_CONTROL.md`                    | Complete documentation                  |

## Testing Your Setup

```python
# Django shell: python manage.py shell

from django.contrib.auth.models import User
user = User.objects.first()
user.profile.role  # 'user', 'admin', or 'superadmin'
user.profile.is_admin()  # True/False
user.profile.is_superadmin()  # True/False
```

## Troubleshooting

| Problem                                    | Solution                                 |
| ------------------------------------------ | ---------------------------------------- |
| User has no profile                        | Run sync_user_roles or create profile    |
| Profile shows "user" but should be "admin" | Use Django Admin to set role             |
| is_staff not matching role                 | Run sync_user_roles for existing users   |
| Template showing wrong content             | Check `profile.is_admin()` vs `is_staff` |

---

**Last Updated:** January 31, 2026  
**System Status:** ✅ Production Ready

# Role-Based Access Control System

## Overview

CampusFix uses a **mutually exclusive role-based access control (RBAC)** system to manage user permissions. This replaces Django's default `is_staff` and `is_superuser` flags with a cleaner, more maintainable approach.

## Role Definition

### User Roles

```
┌─────────────────────────────────────────────────────────────┐
│ ROLE HIERARCHY                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Regular User (user)                                         │
│   └─ Can report issues                                      │
│   └─ Can comment on own issues                              │
│   └─ Can view all issues and their details                  │
│   └─ Can delete own issues                                  │
│                                                              │
│ Administrator (admin)                                       │
│   └─ CANNOT report issues (enforcement in report_issue)    │
│   └─ Can view all issues                                    │
│   └─ Can update issue status (pending, in-progress, etc.)  │
│   └─ Can add admin responses to issues                      │
│   └─ Can comment on any issue                               │
│   └─ Can view contact messages and replies                  │
│   └─ Can soft-delete contact messages                       │
│                                                              │
│ Super Administrator (superadmin)                            │
│   └─ All admin permissions                                  │
│   └─ CANNOT report issues (enforcement in report_issue)    │
│   └─ Can hard-delete contact messages (permanent)           │
│   └─ Can hard-delete contact replies (permanent)            │
│   └─ Access to all admin functions                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### Profile Model (`accounts/models.py`)

```python
class Profile(models.Model):
    ROLE_CHOICES = [
        ("user", "Regular User"),
        ("admin", "Administrator"),
        ("superadmin", "Super Administrator"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    # Helper methods for easy permission checks
    def is_admin(self):
        """Returns True if user is admin or superadmin"""
        return self.role in ["admin", "superadmin"]

    def is_superadmin(self):
        """Returns True if user is superadmin"""
        return self.role == "superadmin"

    def is_regular_user(self):
        """Returns True if user is regular user"""
        return self.role == "user"
```

### Permission Checks in Views

#### Report Issue (Regular Users Only)

**File:** `issues/views.py` → `report_issue()`

```python
if request.user.profile.is_admin():
    messages.error(request, "Administrators cannot report issues...")
    return redirect("dashboard_home")
```

_Business Logic:_ Admins are who fix issues; only regular users should report them.

#### Update Issue Status (Admins Only)

**File:** `issues/views.py` → `update_issue_status()`

```python
if not request.user.profile.is_admin():
    messages.error(request, "You do not have permission to update issue status.")
    return redirect("issue_detail", issue_id=issue.id)
```

#### Delete Contact Messages (SuperAdmins Only)

**File:** `accounts/admin.py` → `hard_delete_messages()`

```python
if not request.user.profile.is_superadmin():
    self.message_user(request, "Only super admins can hard-delete messages.")
    return
```

### Template Checks

#### Display Full Email to SuperAdmins

**File:** `accounts/templates/accounts/contact_view.html`

```django
{% if request.user.profile.is_superadmin %}
    {{ contact.email }}
{% else %}
    {{ contact.email|mask_email }}
{% endif %}
```

#### Show Reported By Name to Admins

**File:** `campusFix/templates/home.html`

```django
{% if user.profile.is_admin %}
    {{ issue.reported_by.get_full_name|default:issue.reported_by.username }}
{% else %}
    Posted by {{ issue.anonymous_code }}
{% endif %}
```

## Admin Management

### Django Admin Interface

Located in `accounts/admin.py`:

#### Profile Admin

- Displays user profiles with role column
- Filter by role
- Can edit role directly

#### User Admin

- Shows role in list view
- Bulk actions to set roles:
  - **Set User Role:** Assigns "user" role
  - **Set Admin Role:** Assigns "admin" role
  - **Set SuperAdmin Role:** Assigns "superadmin" role
- Backward compatible with Django's built-in User model

### Admin Dashboard

**File:** `admin_dashboard/views.py`

Uses the `is_admin` helper function (updated to use `profile.role`):

```python
@user_passes_test(is_admin)
def dashboard_overview(request):
    # Only users with admin role can access
    ...
```

## Migration from Old System

### Existing Users

**Management Command:** `accounts/management/commands/sync_user_roles.py`

Automatically migrates users based on legacy `is_staff`/`is_superuser` flags:

```bash
# Preview changes without applying
python manage.py sync_user_roles --dry-run

# Apply the synchronization
python manage.py sync_user_roles
```

**Mapping:**

- `is_superuser=True` → `role="superadmin"`
- `is_staff=True` → `role="admin"`
- Otherwise → `role="user"`

### New Users

- Default role is "user" (set in Profile model)
- Admin users manually assign roles via Django admin

## Key Changes from Previous System

| Aspect                          | Old                                             | New                               |
| ------------------------------- | ----------------------------------------------- | --------------------------------- |
| **Permission Model**            | `is_staff`, `is_superuser` flags                | `role` field with CHOICES         |
| **Access Checks**               | `request.user.is_staff`                         | `request.user.profile.is_admin()` |
| **Admin Group**                 | Used Django Groups                              | Direct role field                 |
| **Mutually Exclusive**          | No (is_staff + is_superuser could both be True) | Yes (only one role per user)      |
| **Issue Reporting**             | Not restricted for staff                        | Blocked for admins/superadmins    |
| **Contact Message Hard Delete** | Any superuser                                   | SuperAdmins only                  |

## Best Practices

1. **Always use helper methods** when checking permissions:

   ```python
   # ✅ Good
   if request.user.profile.is_admin():

   # ❌ Avoid
   if request.user.is_staff:  # Old system, won't work
   ```

2. **Use role for business logic**:

   ```python
   # Regular users report issues
   # Admins manage/resolve issues
   # Both can comment (but with different permissions)
   ```

3. **Admin panel for role assignment**: Use Django admin instead of manual SQL updates

4. **Log admin actions**: Track when admins update issue status or delete items

## Testing Roles

### Test User Permissions

```python
from django.contrib.auth.models import User
from accounts.models import Profile

# Create test user with specific role
user = User.objects.create_user(username='testuser', password='pass')
user.profile.role = 'admin'
user.profile.save()

# Check permissions
user.profile.is_admin()  # True
user.profile.is_superadmin()  # False
user.profile.is_regular_user()  # False
```

## Summary

The role-based access control system provides:

- ✅ Clear, mutually exclusive roles
- ✅ Easier to audit (one role per user)
- ✅ Business logic enforcement (admins can't report issues)
- ✅ Simple permission checks in views/templates
- ✅ Backward compatible migration path
- ✅ Scalable for future role additions

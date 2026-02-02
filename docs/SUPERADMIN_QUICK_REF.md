# 🛡️ SuperAdmin Login Quick Reference

## Instant Access Links

| Feature                   | URL                                                  | Notes                       |
| ------------------------- | ---------------------------------------------------- | --------------------------- |
| **SuperAdmin Login**      | `http://localhost:8000/accounts/superadmin-login/`   | Username/Password only      |
| **Super Admin Dashboard** | `http://localhost:8000/admin-dashboard/super-admin/` | Full analytics & management |
| **Regular Login**         | `http://localhost:8000/accounts/login/`              | Email/Password for users    |

---

## Your SuperAdmin Account

```
Username: pope
Temporary Password: ChangeMe123!
Email: pope@campusfix.local
```

### First Login

1. Open `/accounts/superadmin-login/`
2. Enter: `pope`
3. Enter: `ChangeMe123!`
4. ✅ Redirected to Super Admin Dashboard

---

## Key Features

### 📊 Dashboard Includes

- 8 Statistics boxes
- 5 Interactive charts (Chart.js)
- User management with role promotion
- Activity logging and failed login tracking
- Top performers leaderboards

### 👥 User Management

- View all users with their roles
- Promote: User → Admin → SuperAdmin
- When promoting to SuperAdmin: **Enter a unique username**
- Activate/Deactivate accounts

### 🔐 SuperAdmin Promotion

**When promoting a user to SuperAdmin:**

1. Select role "SuperAdmin"
2. Browser will prompt for username
3. Enter unique username (e.g., "john_admin")
4. SuperAdmin account created with temporary password

---

## Table of Contents

| File                          | Purpose                                           |
| ----------------------------- | ------------------------------------------------- |
| `SuperAdmin` (DB)             | Stores SuperAdmin credentials (username/password) |
| `SuperAdminLoginForm`         | Username + Password form                          |
| `superadmin_login()` view     | Authentication logic                              |
| `/accounts/superadmin-login/` | URL route                                         |
| `superadmin_login.html`       | Login page (purple gradient)                      |

---

## Important Notes

✅ **Separate Table**: SuperAdmin records separate from Users (no foreign key issues)
✅ **Username Only**: No email needed for SuperAdmin login
✅ **Secure**: Django password hashing (`make_password`, `check_password`)
✅ **Active Flag**: Can deactivate SuperAdmin accounts
✅ **Linked to User**: Each SuperAdmin linked to a User record

---

## Common Tasks

### Change Your Password

```bash
python manage.py shell
```

```python
from accounts.models import SuperAdmin
from django.contrib.auth.hashers import make_password

sa = SuperAdmin.objects.get(username='pope')
sa.password_hash = make_password('NewPassword123!')
sa.save()
```

### Promote a User to SuperAdmin

1. Super Admin Dashboard → Users table
2. Find the user
3. Click role dropdown → Select "SuperAdmin"
4. Enter username when prompted
5. ✅ Done! They get temporary password

### Deactivate a SuperAdmin

1. Super Admin Dashboard → Users table
2. Find the SuperAdmin user
3. Click "Deactivate" button
4. ✅ They can no longer log in

---

## URLs Cheat Sheet

```
/accounts/superadmin-login/           ← SuperAdmin login
/accounts/login/                       ← Regular user login
/accounts/register/                    ← New user registration
/accounts/logout/                      ← Logout
/admin-dashboard/super-admin/          ← Super Admin Dashboard
/admin-dashboard/                      ← Regular Admin Dashboard
/dashboard/                            ← User Dashboard
/issues/                               ← Issue reporting
```

---

## Database

### SuperAdmin Table Structure

```sql
SuperAdmin (
    id,
    user_id (FK to User),
    username (UNIQUE),
    password_hash,
    is_active,
    created_at,
    updated_at
)
```

### Migration Applied

- `0007_superadmin.py` ✅ Applied

---

## Files Modified

✅ `accounts/models.py` - SuperAdmin model added
✅ `accounts/forms.py` - SuperAdminLoginForm added  
✅ `accounts/views.py` - superadmin_login view added
✅ `accounts/urls.py` - /superadmin-login/ route added
✅ `admin_dashboard/views.py` - promote_user updated
✅ `admin_dashboard/templates/super_admin.html` - username field added
✅ `campusFix/urls.py` - Django admin removed
✅ `campusFix/templates/layout.html` - Already showing SuperAdmin link

---

## Troubleshooting

**"Invalid username or password"**

- Check spelling of username (case-sensitive)
- Verify account is active (not deactivated)
- Check password is correct

**"Username already taken"**

- Choose a different unique username
- Or check if SuperAdmin already exists for this user

**"SuperAdmin account not properly linked"**

- SuperAdmin record exists but user field is null
- Contact developer to fix linking

---

## Support

For issues or questions, refer to:

- `SUPERADMIN_LOGIN_SETUP.md` - Full documentation
- `admin_dashboard/templates/admin_dashboard/super_admin.html` - Dashboard template
- `accounts/views.py` - Login logic
- `accounts/models.py` - SuperAdmin model definition

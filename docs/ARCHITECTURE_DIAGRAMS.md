# 🏗️ SuperAdmin Login System - Architecture & Flow Diagrams

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CampusFix Platform                          │
└─────────────────────────────────────────────────────────────────┘

                    Login Options
                         │
            ┌────────────┼────────────┐
            │            │            │
            ▼            ▼            ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │ Regular User │ │    Admin     │ │  SuperAdmin  │
    │    Login     │ │    Login     │ │    Login     │
    │              │ │  (via User)  │ │ (via Super   │
    │ Email + Pwd  │ │              │ │  Admin Table)│
    │              │ │ Email + Pwd  │ │              │
    └──────────────┘ └──────────────┘ │Username+Pwd  │
         │                │            └──────────────┘
         │                │                    │
         ▼                ▼                    ▼
    ┌────────────────────────────────────────────────┐
    │       Authentication System                    │
    │  ┌──────────────────────────────────────────┐  │
    │  │  User Table (Django auth_user)           │  │
    │  │  ├─ username (email-based)               │  │
    │  │  ├─ email                                │  │
    │  │  ├─ password                             │  │
    │  │  └─ is_active                            │  │
    │  └──────────────────────────────────────────┘  │
    │                     ↑                           │
    │  ┌──────────────────────────────────────────┐  │
    │  │  Profile Table (Extended User Info)      │  │
    │  │  ├─ user (OneToOne FK)                   │  │
    │  │  ├─ role (user/admin/superadmin)         │  │
    │  │  ├─ name                                 │  │
    │  │  └─ is_verified                          │  │
    │  └──────────────────────────────────────────┘  │
    │                                                 │
    │  ┌──────────────────────────────────────────┐  │
    │  │  SuperAdmin Table (NEW - Separate)       │  │
    │  │  ├─ username (unique)                    │  │
    │  │  ├─ password_hash                        │  │
    │  │  ├─ user (FK to User - optional)         │  │
    │  │  ├─ is_active                            │  │
    │  │  ├─ created_at                           │  │
    │  │  └─ updated_at                           │  │
    │  └──────────────────────────────────────────┘  │
    └────────────────────────────────────────────────┘
         │                │                │
         ▼                ▼                ▼
    [User          [Admin          [SuperAdmin
     Dashboard]    Dashboard]      Dashboard]
```

---

## Authentication Flow Diagram

### Regular User/Admin Login

```
┌─────────────────────────────────────┐
│ User enters Email + Password         │
│ URL: /accounts/login/               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Django authenticate()                │
│ Checks: User table                  │
│ - username = email                  │
│ - password matches                  │
└────────────┬────────────────────────┘
             │
             ▼
         (Success?)
         │       │
         │       └──→ ❌ Error Message
         │            "Invalid email/password"
         │
         ▼
    ✅ login() function
    Creates session
         │
         ▼
    Check Profile.role
    │       │
    ├──→ admin → Admin Dashboard
    └──→ user  → User Dashboard
```

### SuperAdmin Login (NEW)

```
┌─────────────────────────────────────┐
│ SuperAdmin enters Username + Password│
│ URL: /accounts/superadmin-login/    │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Query SuperAdmin table               │
│ - username = input username         │
│ - is_active = True                  │
└────────────┬────────────────────────┘
             │
             ▼
         (Found?)
         │       │
         │       └──→ ❌ "Invalid username/password"
         │
         ▼
    ✅ check_password()
    Verify password_hash
         │
         ▼
     (Correct?)
     │       │
     │       └──→ ❌ "Invalid username/password"
     │
     ▼
Get linked User from SuperAdmin.user
     │
     ▼
login(request, user)
Creates Django session
     │
     ▼
Redirect to super_admin_dashboard
     │
     ▼
✅ [Super Admin Dashboard]
```

---

## Database Relationship Diagram

```
┌──────────────────────────┐
│      auth_user           │
│   (Django Default)       │
├──────────────────────────┤
│ id (PK)                  │
│ username (email-based)   │
│ password (hash)          │
│ email                    │
│ is_active                │
│ created_at               │
└──────────────────────────┘
         │
         │ OneToOne
         ├─────────────────────────────┐
         │                             │
         ▼                             ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│      accounts.Profile    │  │  accounts.SuperAdmin     │
│     (Extended Info)      │  │     (NEW TABLE)          │
├──────────────────────────┤  ├──────────────────────────┤
│ id (PK)                  │  │ id (PK)                  │
│ user_id (FK) ────────────┼─→│ user_id (FK) - OPTIONAL │
│ role                     │  │ username (UNIQUE)        │
│ name                     │  │ password_hash            │
│ is_verified              │  │ is_active                │
│ created_at               │  │ created_at               │
│ updated_at               │  │ updated_at               │
└──────────────────────────┘  └──────────────────────────┘
```

### Key Relationships

- **User ↔ Profile**: OneToOne (required)
- **User ↔ SuperAdmin**: OneToOne (optional)
- **Why optional?** Allows flexibility for future enhancements

---

## User Promotion Flow Diagram

```
┌──────────────────────────────────────────────┐
│ SuperAdmin Dashboard → Users Table            │
│ Selects user and changes role to "SuperAdmin"│
└────────────┬─────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────┐
│ JavaScript prompt() dialog appears            │
│ "Enter a unique username for this SuperAdmin:"│
└────────────┬─────────────────────────────────┘
             │
             ▼
    (Username entered?)
    │                │
    │                └──→ ❌ Cancelled
    │                     (no change)
    │
    ▼
┌──────────────────────────────────────────────┐
│ promote_user() view receives:                │
│ - user_id                                    │
│ - role = "superadmin"                        │
│ - superadmin_username                        │
└────────────┬─────────────────────────────────┘
             │
             ▼
    Update User.profile.role = "superadmin"
             │
             ▼
    Check username uniqueness
    │                    │
    │                    └──→ ❌ Error
    │                         "Username taken"
    │
    ▼
┌──────────────────────────────────────────────┐
│ Create SuperAdmin record:                    │
│ - username = input username                  │
│ - password_hash = make_password("ChangeMe...") │
│ - user = User object                         │
│ - is_active = True                           │
└────────────┬─────────────────────────────────┘
             │
             ▼
    ✅ Success Message
    "User promoted to SuperAdmin"
    │
    ▼
Redirect to super_admin_dashboard
```

---

## Permission & Access Control Diagram

```
Anonymous User
    │
    ├─→ Can access: /accounts/login/
    ├─→ Can access: /accounts/superadmin-login/
    ├─→ Can access: /accounts/register/
    └─→ Cannot access: /admin-dashboard/*

Regular User (profile.role = "user")
    │
    ├─→ Can access: /dashboard/
    ├─→ Can access: /issues/
    └─→ Cannot access: /admin-dashboard/*

Admin (profile.role = "admin")
    │
    ├─→ Can access: /admin-dashboard/
    │    (Dashboard overview, issue management, etc)
    └─→ Cannot access: /admin-dashboard/super-admin/

SuperAdmin (profile.role = "superadmin")
    │
    ├─→ Can access: /admin-dashboard/super-admin/
    │    (Full system management, user management, analytics)
    ├─→ Can access: /accounts/superadmin-login/
    └─→ Can promote other users to SuperAdmin
```

---

## Login Page Navigation Diagram

```
┌────────────────────────────────────┐
│   Unauthenticated User              │
│   (No active session)               │
└────────────┬───────────────────────┘
             │
             ▼
    Navigation Bar Shows:
    ├─ 📝 Register
    ├─ 👤 Login
    └─ 🛡️ SuperAdmin Login
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────┐  ┌────┐  ┌──────────────┐
│Reg.│  │Log.│  │SuperAdmin    │
│    │  │    │  │Login         │
└────┘  └────┘  └──────────────┘
  │       │           │
  │       │           ▼
  │       │    [SuperAdmin Form]
  │       │    username + password
  │       │           │
  │       │           ▼
  │       │    [Super Admin Dashboard]
  │       │
  │       ▼
  │    [User Login Form]
  │    email + password
  │       │
  │       ▼
  │    Check Profile.role
  │    │                  │
  │    ├→ admin → [Admin Dashboard]
  │    └→ user  → [User Dashboard]
  │
  ▼
[Registration Form]
name + email + password
     │
     ▼
[Email Verification]
     │
     ▼
[User Dashboard]
```

---

## Data Flow on SuperAdmin Login

```
Input:
  username = "pope"
  password = "ChangeMe123!"

          │
          ▼
    ┌──────────────────┐
    │ superadmin_login │
    │      view        │
    └────────┬─────────┘
             │
             ▼
    SuperAdmin.objects.get(
      username='pope',
      is_active=True
    )
             │
             ▼
    Found SuperAdmin object:
      id: 1
      username: "pope"
      password_hash: "$2b$12$..."  ← bcrypt hash
      user_id: 3                    ← links to User
      is_active: True
             │
             ▼
    check_password("ChangeMe123!", password_hash)
             │
             ▼
    Returns: True ✅
             │
             ▼
    Get linked User:
      User.objects.get(id=3)
             │
             ▼
    User object:
      id: 3
      username: "pope"
      email: "pope@campusfix.local"
      is_active: True
      profile.role: "superadmin"
             │
             ▼
    login(request, user)
    Creates session with user_id=3
             │
             ▼
    Redirect to /admin-dashboard/super-admin/
             │
             ▼
    Super Admin Dashboard loads
    All admin features available
```

---

## Technology Stack

```
Frontend
├─ HTML5
├─ CSS3 (Purple gradient design)
├─ JavaScript (form handling)
└─ Django Templates

Backend
├─ Django 6.0.1
├─ Python 3.12
├─ Django ORM
└─ Django Auth System

Database
├─ PostgreSQL (or SQLite in dev)
├─ Django Models
├─ Foreign Keys
└─ Migrations

Security
├─ Django password hashing (PBKDF2)
├─ CSRF protection
├─ Session management
└─ Password validation
```

---

## Summary

The SuperAdmin login system creates:

- ✅ **Separate authentication path** for superadmins
- ✅ **Isolated credentials** in dedicated table
- ✅ **Secure password hashing** with Django's system
- ✅ **Clean separation** between user & admin auth
- ✅ **Scalable architecture** for future extensions
- ✅ **Professional UI** matching admin dashboard design

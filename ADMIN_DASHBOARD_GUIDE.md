# CampusFix Admin Dashboard - Complete Documentation

## Overview

The Admin Dashboard is a specialized interface for operational admins (non-superadmins) to manage campus issues and maintain system functionality without having system-level control.

---

## Admin Role & Permissions

### What Admins Can Do ✅

- **View Issues**: Access all submitted issues with filtering by status, category, and priority
- **Manage Issue Status**: Update issue status (Pending → In Progress → Resolved)
- **Add Official Responses**: Post official comments/responses to issues
- **Request Information**: Ask users for additional details about their issues
- **View Activity Logs**: See a record of all actions taken (for accountability)
- **View User Information**: Access basic info (name, submission history) but NOT:
  - Passwords
  - Authentication data
  - User account management
  - System settings
  - Permissions/roles

### What Admins Cannot Do ❌

- Delete users
- Reset user passwords
- Modify system settings
- Change user permissions or roles
- Delete or alter activity logs
- Access authentication data
- Modify core system behavior

---

## Dashboard Pages

### 1. Admin Dashboard Overview

**URL**: `/admin-dashboard/`

#### Features:

- **Quick Metrics**:
  - Total Issues
  - Pending Issues
  - In Progress Issues
  - Resolved Issues
- **Recent Issues**: Latest 5 issues submitted
- **Recent Activity**: Your last 5 admin actions

### 2. Issues Management

**URL**: `/admin-dashboard/issues/`

#### Features:

- **Advanced Filtering**:
  - Search by title/description
  - Filter by status (Pending, In Progress, Resolved)
  - Filter by category
  - Filter by priority
- **Issue Table**: Shows ID, Title, Category, Priority, Status, Reporter, Date, Comments Count
- **Pagination**: 10 issues per page
- **Quick Actions**: View details

#### Column Information:

- **ID**: Unique issue identifier
- **Title**: Issue title
- **Category**: Issue category (Maintenance, IT, Facilities, etc.)
- **Priority**: Issue urgency level
- **Status**: Current state of the issue
- **Reporter**: User who reported (display name only, no contact info)
- **Date**: When the issue was submitted
- **Comments**: Number of responses/comments

### 3. Issue Details & Management

**URL**: `/admin-dashboard/issues/<issue_id>/`

#### Sections:

##### Issue Details Card

- Issue ID
- Title
- Status (with color-coded badge)
- Category
- Priority
- Location
- Reporter Name
- Date Reported
- Full Description

##### Update Status Section

- Dropdown to change status
- Submit button to save changes
- Logs the action automatically

##### Comments & Updates Section

- View all user comments
- View all admin responses (marked with "Admin" badge)
- See comment timestamps
- Track conversation history

##### Add Official Response Section

- Text area for admin response
- Response is marked as official admin response
- Visible to the issue reporter
- Automatically logged in activity

##### Quick Info Sidebar

- Issue ID
- Total Comments Count
- Days Since Submission

---

## Activity Log

**URL**: `/admin-dashboard/activity-log/`

### Features:

- **Track All Admin Actions**: View all actions taken by any admin
- **Action History**:
  - Timestamp
  - Admin who performed action
  - Issue involved
  - Action performed
- **Accountability**: Complete audit trail for compliance
- **Pagination**: 20 activities per page

### Logged Actions:

- Status updates
- Official responses added
- Information requests

---

## How to Use the Admin Dashboard

### Accessing the Dashboard

1. **Login** with an admin account
2. **Navigation**: Admin accounts will see "👨‍💼 Admin Dashboard" in the navigation instead of "Dashboard"
3. Click it to access the admin dashboard

### Daily Workflow

#### Morning: Review Overview

1. Check dashboard overview for key metrics
2. Identify pending issues that need attention
3. Review recent activity from other admins

#### Managing Issues

1. Go to Issues Management
2. Filter by status (e.g., "Pending" to find new issues)
3. Sort by priority to identify urgent issues
4. Click "View" to open issue details

#### Handling an Issue

1. Read the issue description and location
2. Check existing comments/responses
3. Update status if needed:
   - "Pending" → "In Progress" when starting work
   - "In Progress" → "Resolved" when fixed
4. Add official response if needed
5. Close the issue when resolved

#### Accountability

- All your actions are logged in Activity Log
- Other admins can see what you did and when
- This maintains transparency and accountability

---

## Status Definitions

- **Pending**: Issue just reported, awaiting review
- **In Progress**: Issue being worked on
- **Resolved**: Issue has been fixed/addressed

---

## Best Practices

### Communication

- Always add official responses for clarity
- Be professional in all comments
- Request specific information if needed

### Issue Management

- Prioritize high-priority issues
- Follow up on in-progress issues
- Close resolved issues promptly

### Accountability

- Your actions are logged for auditing purposes
- Be transparent about what actions you take
- Review activity logs regularly

---

## Technical Information

### Models Used

**AdminActivity Model**

- Records all admin actions
- Stores: Admin user, Issue, Action description, Timestamp
- Used for accountability and audit trails

**IssueComment Model** (Enhanced)

- Added `is_admin_response` field
- Distinguishes admin official responses from regular comments

### Permissions

- Admins belong to the "Admins" group
- Access protected by `@user_passes_test(is_admin)` decorator
- Automatic redirection for non-admin users

---

## Troubleshooting

### Can't Access Admin Dashboard?

- Verify you're in the "Admins" group
- Ensure `is_staff` is set to True
- Re-login after group assignment

### Need to Grant Admin Access?

```bash
python manage.py shell
from django.contrib.auth.models import User, Group

# Get admin group (creates if doesn't exist)
admin_group, created = Group.objects.get_or_create(name='Admins')

# Get user
user = User.objects.get(username='username')

# Add to group
user.groups.add(admin_group)
user.is_staff = True
user.save()
```

---

## Security Notes

- ✅ Admins cannot see/modify passwords
- ✅ Admins cannot delete users
- ✅ Admins cannot change system permissions
- ✅ All actions are logged and auditable
- ✅ Admin access is verified on every page
- ✅ Non-sensitive user information only

---

## Support

For issues or questions about the admin dashboard, contact:

- Technical Support: [contact info]
- Documentation: [docs location]

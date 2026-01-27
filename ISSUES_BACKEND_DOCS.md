# Issues App - Backend Documentation

## Overview

Complete backend implementation for the campus issues management system with full validation, filtering, and admin capabilities.

---

## Database Models

### Issue Model

**Purpose:** Stores information about reported issues

**Fields:**

- `title` (CharField, 200 chars) - Issue title (required)
- `description` (TextField) - Detailed description (required)
- `category` (CharField) - Issue category (Maintenance, IT, Facilities, Cleanliness, Security, Other)
- `priority` (CharField) - Priority level (Low, Medium, High, Critical)
- `status` (CharField) - Current status (Pending, In Progress, Resolved, Rejected)
- `reported_by` (ForeignKey) - User who reported the issue
- `attachment` (ImageField) - Optional image attachment (max 5MB, JPG/PNG/GIF only)
- `created_at` (DateTimeField) - Auto-generated timestamp
- `updated_at` (DateTimeField) - Auto-updated timestamp
- `admin_notes` (TextField) - Notes for admins (optional)
- `assigned_to` (ForeignKey) - Staff member assigned to resolve (optional)

**Methods:**

- `is_urgent()` - Returns True if priority is High or Critical

**Indexes:**

- Status + Created Date (for faster queries)
- Category + Status (for filtering)

---

### IssueComment Model

**Purpose:** Stores comments/updates on issues

**Fields:**

- `issue` (ForeignKey) - Related issue
- `author` (ForeignKey) - User who commented
- `content` (TextField) - Comment text
- `created_at` (DateTimeField) - Auto-generated timestamp
- `updated_at` (DateTimeField) - Auto-updated timestamp

---

## Forms

### ReportIssueForm

**Purpose:** Validates issue submission data

**Validation:**

- Title: Minimum 5 characters
- Description: Minimum 10 characters
- Attachment: Maximum 5MB, only image files (JPG, PNG, GIF)

**Fields:**

- title
- category
- description
- priority
- attachment

---

### UpdateIssueStatusForm

**Purpose:** Allows admins to update issue status and notes

**Fields:**

- status
- admin_notes
- assigned_to

---

### IssueCommentForm

**Purpose:** Validates comment submissions

**Validation:**

- Content: 2-1000 characters

**Fields:**

- content

---

### IssueFilterForm

**Purpose:** Filters issues by status, category, or search term

**Fields:**

- status (optional filter)
- category (optional filter)
- search (text search in title and description)

---

## Views

### 1. report_issue() - POST/GET

**URL:** `/issues/report/`
**Permission:** Login required
**Description:** Form to report new issue

- GET: Display form
- POST: Submit and create issue
- Redirects to issue detail on success
- Shows error messages for validation failures

---

### 2. issue_list() - GET

**URL:** `/issues/`
**Permission:** Login required
**Description:** Display all issues with filtering and pagination

- Lists all issues in system
- Supports filtering by status, category, search
- 10 issues per page
- Shows total issue count

---

### 3. my_issues() - GET

**URL:** `/issues/my-issues/`
**Permission:** Login required
**Description:** Display only current user's reported issues

- Lists only issues reported by logged-in user
- Supports same filtering as issue_list()
- Paginated (10 per page)

---

### 4. issue_detail() - GET/POST

**URL:** `/issues/<issue_id>/`
**Permission:** Login required
**Description:** Display issue details and handle comments

- GET: Show issue details and comments
- POST: Add new comment (requires login)
- Only issue reporter and staff can edit

---

### 5. delete_issue() - GET/POST

**URL:** `/issues/<issue_id>/delete/`
**Permission:** Login required (issue reporter or staff only)
**Description:** Delete an issue

- GET: Show confirmation page
- POST: Confirm and delete
- Only reporter or staff can delete
- Redirects to my_issues or issue_list after delete

---

### 6. update_issue_status() - GET/POST

**URL:** `/issues/<issue_id>/update-status/`
**Permission:** Staff/Admin only
**Description:** Update issue status (admin function)

- GET: Show status update form
- POST: Update issue with new status and notes
- Can assign to staff member
- Only accessible to staff users

---

## URL Routes

```
/issues/                           - List all issues
/issues/report/                    - Report new issue
/issues/my-issues/                 - My reported issues
/issues/<id>/                      - Issue details & comments
/issues/<id>/delete/               - Delete issue
/issues/<id>/update-status/        - Update status (admin)
```

---

## Validation Rules

### Title

- ✓ Required
- ✓ Minimum 5 characters
- ✓ Maximum 200 characters

### Description

- ✓ Required
- ✓ Minimum 10 characters

### Category

- ✓ Required
- ✓ Must be: Maintenance, IT, Facilities, Cleanliness, Security, or Other

### Priority

- ✓ Required
- ✓ Must be: Low, Medium, High, or Critical

### Attachment

- ✓ Optional
- ✓ Maximum 5MB file size
- ✓ Only JPG, JPEG, PNG, GIF allowed
- ✓ File name validation

### Comment

- ✓ Required
- ✓ Minimum 2 characters
- ✓ Maximum 1000 characters

---

## Admin Interface

### Issue Admin

- View all issues
- Filter by: status, category, priority, date
- Search by: title, description, reporter email
- Edit status, admin notes, assignment
- View attachments

### IssueComment Admin

- View all comments
- Filter by: date, issue
- Search by: content, author, issue title
- Track comment history

---

## Security Features

✅ Login required for all views
✅ Permission checks (only allow issue reporter/staff to edit)
✅ File validation (size, type, extension)
✅ CSRF protection on all forms
✅ Proper error handling and messages
✅ Read-only timestamps

---

## Database Queries Optimized

- Indexed status + created_date for fast lookups
- Indexed category + status for filtering
- Foreign key relationships for data integrity
- Pagination to limit database load

---

## Error Handling

- Form validation errors displayed to user
- File upload errors with specific messages
- Permission denied messages
- Missing issue (404 error)
- Success/error messages using Django messages framework

---

## Testing Checklist

- [ ] Report issue with valid data
- [ ] Report issue with invalid title (< 5 chars)
- [ ] Report issue with invalid description (< 10 chars)
- [ ] Upload file > 5MB (should fail)
- [ ] Upload non-image file (should fail)
- [ ] View all issues list
- [ ] Filter issues by status
- [ ] Filter issues by category
- [ ] Search issues
- [ ] View my reported issues
- [ ] View issue details
- [ ] Add comment to issue
- [ ] Delete own issue
- [ ] Try to delete others' issue (should fail)
- [ ] Admin: Update issue status
- [ ] Admin: Assign issue to staff

---

## Future Enhancements

- [ ] Email notifications when issue status changes
- [ ] File storage cleanup for deleted issues
- [ ] Bulk actions (mark multiple as resolved)
- [ ] Issue priority auto-escalation
- [ ] Tags/labels for better organization
- [ ] Issue duplicate detection
- [ ] Resolution time tracking
- [ ] User feedback/rating on resolution

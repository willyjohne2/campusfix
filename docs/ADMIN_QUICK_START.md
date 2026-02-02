# Admin Dashboard - Quick Reference

## 🎯 Quick Start

1. **Login** with admin credentials
2. You'll be **automatically redirected** to Admin Dashboard
3. See menu with: "👨‍💼 Admin Dashboard" instead of "Dashboard"

---

## 📊 Dashboard Pages

| Page         | URL                              | Purpose                |
| ------------ | -------------------------------- | ---------------------- |
| Overview     | `/admin-dashboard/`              | Quick stats & metrics  |
| Issues       | `/admin-dashboard/issues/`       | Browse & filter issues |
| Issue Detail | `/admin-dashboard/issues/<id>/`  | Manage single issue    |
| Activity Log | `/admin-dashboard/activity-log/` | View audit trail       |

---

## 🔍 Filtering Issues

**Available Filters:**

- 🔎 **Search** - Title/Description
- 📌 **Status** - Pending, In Progress, Resolved
- 🏷️ **Category** - Maintenance, IT, Facilities, Cleanliness, Security
- ⚡ **Priority** - High, Medium, Low

**Tip:** Combine filters for precise results!

---

## 📋 Issue Detail View

### What You See:

- Issue title & ID
- Full description
- Location & category
- Status & priority
- Reporter name (no contact info)
- Date submitted

### What You Can Do:

1. **Update Status** - Change from Pending → In Progress → Resolved
2. **Add Response** - Post official admin response
3. **View Comments** - See all conversation
4. **Check Activity** - See days issue has been open

---

## 🎬 Status Workflow

```
Reported
   ↓
[Pending] ← Initial state
   ↓
[In Progress] ← You're working on it
   ↓
[Resolved] ← Issue fixed
```

---

## 👤 User Info Access

### ✅ You CAN See:

- Display name
- Submission history
- When they reported the issue
- Issue details they provided

### ❌ You CANNOT See:

- Email address (from admin view)
- Password
- Account credentials
- Personal data beyond report
- Delete or modify user accounts

---

## 📝 Response Best Practices

**DO:**

- ✅ Be professional and clear
- ✅ Provide specific next steps
- ✅ Request exact information if needed
- ✅ Update status before closing
- ✅ Check existing comments first

**DON'T:**

- ❌ Share personal info
- ❌ Make promises you can't keep
- ❌ Ignore urgent issues
- ❌ Delete or modify responses
- ❌ Mark resolved without confirming

---

## 🔐 Activity Log

**Auto-Logged Actions:**

- Status updates
- Official responses added
- Information requests

**Use For:**

- Transparency
- Accountability
- Reviewing past actions
- Training new admins

---

## ⚙️ Common Tasks

### Handle New Issue

1. Go to Issues → Filter: Pending
2. Click "View" on issue
3. Read description & location
4. Update status → "In Progress"
5. Add response with next steps

### Follow Up

1. Go to Issues → Filter: In Progress
2. Click issues to check for user responses
3. Add response if needed
4. Update status when fixed

### Mark Resolved

1. Open issue detail
2. Update status → "Resolved"
3. Add final response if needed
4. Done! ✓

---

## 🆘 Troubleshooting

**Can't see Admin Dashboard link?**

- Not in "Admins" group
- Ask super admin to add you

**Can't update status?**

- Check if you're logged in as admin
- Refresh page if button not responding

**Response not showing?**

- Check if you're viewing latest comments
- Refresh page to see updates

---

## 📞 Key Contacts

- **Super Admin** - System settings & user management
- **IT Support** - Technical issues
- **Help Desk** - General questions

---

## 🎨 Color Coding Guide

| Color     | Meaning                       |
| --------- | ----------------------------- |
| 🟠 Orange | Pending (needs attention)     |
| 🔵 Blue   | In Progress (being worked on) |
| 🟢 Green  | Resolved (fixed)              |
| 🟣 Purple | High Priority                 |
| 🟡 Yellow | Medium Priority               |
| 🔴 Red    | Low Priority                  |

---

## ⌨️ Keyboard Tips

- **Tab** - Navigate between fields
- **Enter** - Submit forms
- **Ctrl+F** - Search page content
- **Esc** - Close modals (if any)

---

## 📱 Mobile Tips

- Scroll tables horizontally
- Use Search filter on mobile
- Tap badges for info
- One action per screen for clarity

---

**Need Help?** Check `ADMIN_DASHBOARD_GUIDE.md` for detailed information!

**Last Updated:** January 21, 2026

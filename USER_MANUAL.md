# LeaveOk — User Manual
**Smart Leave Management System**

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Student / Employee Guide](#2-student--employee-guide)
3. [Faculty / Manager Guide](#3-faculty--manager-guide)
4. [Admin Guide](#4-admin-guide)
5. [Common Features](#5-common-features)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Getting Started

### Accessing the System

Open any modern web browser (Chrome, Firefox, Edge, Safari) and go to:

```
http://<server-ip>:5000
```

If running locally: `http://localhost:5000`  
On a network: ask your administrator for the server IP address.

---

### Registering an Account

1. On the home page, click **Register**
2. Fill in:
   - **Full Name** — your real name
   - **Email** — must be unique in the system
   - **Password** — choose a secure password
   - **Role** — select your role:
     - `Student` — to apply for leave
     - `Faculty` — to review and approve/reject student leaves
     - `Admin` — full system access
3. Click **Register**
4. You will be redirected to the login page

> If you see "Email already registered", use a different email or go to Login.

---

### Logging In

1. Go to the home page and click **Login**
2. Enter your **Email** and **Password**
3. Click **Login**
4. You will be automatically redirected to your role's dashboard

> If credentials are wrong, an error message appears — check your email/password.

---

### Logging Out

Click **Logout** in the bottom-left sidebar on any page.  
Your session is fully cleared — no one can access your account by pressing the back button.

---

## 2. Student / Employee Guide

After login you land on the **Student Dashboard**.

---

### Dashboard Overview

The dashboard shows 4 stat cards:

| Card | Meaning |
|------|---------|
| Total Leaves | All leave requests you have submitted |
| Approved | Leaves fully approved by Faculty + Admin |
| Pending | Leaves still awaiting a decision |
| Rejected | Leaves that were rejected |

Quick action buttons at the bottom let you jump to Apply, History, or Status.

---

### Applying for Leave

1. Click **Apply Leave** in the sidebar
2. Fill in the form:
   - **Leave Type** — Sick Leave / Casual Leave / Emergency Leave / Other
   - **From Date** — start date of your leave
   - **To Date** — end date (must be on or after From Date)
   - **Reason** — describe why you need leave
3. Click **Submit Application**

Your leave enters the approval pipeline with status **Pending**.

> All fields are required. If From Date is after To Date, an error will appear.

---

### Checking Leave History

Click **Leave History** in the sidebar to see all your submitted leaves in a table showing:

- Leave Type, From, To dates
- **Faculty** decision (Pending / Approved / Rejected)
- **Admin** decision (Pending / Approved / Rejected / N/A)
- **Final Status**

---

### Tracking Leave Status

Click **Leave Status** in the sidebar for a detailed pipeline view of each leave:

```
Student → Faculty → Admin
```

Each card shows:
- The leave type and date range
- The final status badge (Pending / Approved / Rejected)
- Faculty's decision + name + remark
- Admin's final decision + remark

> If Faculty rejects, Admin shows **N/A** — the process ends at Faculty.

---

### Managing Your Profile

Click **Profile** in the sidebar. Three tabs are available:

**Personal Info tab**
- Update your name, email, phone number, department, and bio
- Click **Save Changes**

**Change Password tab**
- Enter your current password
- Enter and confirm your new password
- A live indicator shows if passwords match
- Click **Update Password**

**Account tab**
- View your User ID, role, and registered email
- **Danger Zone** — Logout button to sign out

---

## 3. Faculty / Manager Guide

After login you land on the **Faculty Dashboard**.

---

### Dashboard Overview

4 stat cards show:

| Card | Meaning |
|------|---------|
| Awaiting Your Review | Leaves pending your decision |
| You Approved | Leaves you forwarded to Admin |
| You Rejected | Leaves you rejected (final) |
| Total Reviewed | Approved + Rejected count |

A blue info banner reminds you of the approval flow:  
**Student submits → You review → Admin gives final decision**

The table below shows the 10 most recent pending leaves for quick action.

---

### Reviewing Leave Requests

1. Click **Leave Requests** in the sidebar
2. The table shows all leave requests with your decision status
3. Use the **search box** to find a student by name
4. Use the **status filter** to show only Pending / Approved / Rejected

**To approve or reject a leave:**

1. Click **✓ Approve** or **✕ Reject** on any Pending row
2. A modal dialog opens showing the student's details
3. Optionally type a **remark** (e.g. reason for rejection)
4. Click **✓ Approve & Forward** or **✕ Confirm Rejection**

> **Approving** forwards the leave to Admin for final decision.  
> **Rejecting** is final — Admin is not involved.

Once approved, the row shows **→ Forwarded to Admin**.

---

## 4. Admin Guide

After login you land on the **Admin Dashboard**.

---

### Dashboard Overview

4 stat cards show system-wide stats:

| Card | Meaning |
|------|---------|
| Total Users | All registered accounts |
| Total Leaves | All leave requests in the system |
| Awaiting Your Decision | Faculty-approved leaves needing your action |
| Finally Approved | Leaves you have fully approved |

The **Three-Level Approval Overview** progress bars show the percentage of leaves that are Approved / Awaiting / Rejected across the whole system.

The **Recent Leave Requests** table shows the latest 10 leaves with quick approve/reject buttons.

---

### Managing Leave Requests

Click **Leaves** in the sidebar to see all leave requests.

**Filtering:**
- Click **⚡ Awaiting Only** to see only Faculty-approved leaves that need your decision (highlighted in yellow)
- Click **All Leaves** to see everything
- Use the **search box** to find a user by name
- Use the **status dropdown** to filter by Final Status

**To approve or reject:**

1. Click **✓** (approve) or **✕** (reject) on an awaiting row
2. A modal opens — optionally add an **Admin Remark**
3. Click **✓ Approve** or **✕ Reject** to confirm

> Only leaves where Faculty has already approved will show action buttons.

---

### Managing Users

Click **Users** in the sidebar to see all registered accounts.

The table shows:
- User ID, Name, Email
- Role badge — color-coded:
  - 🟣 **Admin** (purple)
  - 🟡 **Faculty** (yellow)
  - 🟢 **Student** (green)

Use the **search box** to filter by name or email.

---

### Awaiting Approval Shortcut

The sidebar shows a red badge on **Awaiting Approval** with the count of leaves needing your action. Click it to jump directly to the filtered view.

---

## 5. Common Features

### Navigation Sidebar

Every page has a sidebar with:
- Your role's navigation links
- The active page is highlighted in blue
- **Logout** at the bottom

### Session Security

- You cannot access another role's pages — you will be redirected to your own dashboard
- Pressing the browser back button after logout will not show protected pages
- Touchpad swipe-back is also blocked

### Status Badges

| Badge | Color | Meaning |
|-------|-------|---------|
| Pending | Yellow | Awaiting a decision |
| Approved | Green | Approved at this stage |
| Rejected | Red | Rejected at this stage |
| N/A | Grey | Not applicable (Faculty rejected, Admin skipped) |

---

## 6. Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't log in | Check email/password. Ensure Caps Lock is off. |
| "Email already registered" | Use a different email or go to Login |
| Leave form won't submit | All fields are required. Check dates are valid. |
| Redirected to login unexpectedly | Your session expired — log in again |
| Page shows old data after logout | Clear browser cache or use Ctrl+Shift+R |
| Can't reach the site on network | Ask admin for the correct IP. Check port 5000 is open. |
| Approve/Reject button not showing | Leave must be Faculty-approved first before Admin can act |

---

*LeaveOk — Smart Leave Management System*

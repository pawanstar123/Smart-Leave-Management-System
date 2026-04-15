# LeaveOk — Smart Leave Management System

A three-level role-based leave management web app built with Flask and MySQL.
Students apply for leaves → Faculty reviews first → Admin gives the final decision.

---

## Approval Flow

```
Student applies
      ↓
Faculty reviews  →  Rejects (final, no Admin needed)
      ↓ Approves
Admin reviews    →  Approves / Rejects (final decision)
      ↓
Student sees final status with both remarks
```

---
##  Overview

LeaveOk is a role-based Smart Leave Management System designed to streamline the leave application and approval process in academic institutions.

It provides separate dashboards for Students, Faculty, and Admin, ensuring efficient leave tracking, approval workflows, and system transparency.
## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3, Vanilla JS |
| Database | MySQL |
| DB Driver | mysql-connector-python |
| Styling | Custom CSS — dark sidebar theme, no frameworks |
| Sessions | Flask server-side sessions |

---

## Project Structure

```
LeaveOk/
├── app.py                              # All routes, DB logic, auto-reconnect helper
├── README.md
│
├── static/
│   └── style.css                       # Global stylesheet (shared across all pages)
│
└── templates/
    ├── home.html                       # Landing page
    ├── login.html                      # Login
    ├── register.html                   # Register (Student / Faculty / Admin)
    │
    ├── user Dashboard/
    │   ├── user_dashboard.html         # Stats + quick actions
    │   ├── apply_leave.html            # Leave application form
    │   ├── leave_history.html          # Leave table with Faculty + Admin stage columns
    │   ├── leave_status.html           # Visual pipeline — Student → Faculty → Admin
    │   └── user_profile.html           # Tabbed profile — info, password, account
    │
    ├── faculty Dashboard/
    │   ├── Faculty_Dashboard.html      # Pending count, quick approve/reject, flow note
    │   └── Faculty_Leave.html          # Full table with remarks modal, forwarding note
    │
    └── admin Dashboard/
        ├── admin_dashboard.html        # Stats, progress bars, recent leaves pipeline view
        ├── admin_leaves.html           # Full table — Faculty + Admin columns, awaiting filter
        └── admin_users.html            # All registered users with search
```

---

## Database Schema

```sql
CREATE DATABASE leave_system;
USE leave_system;

CREATE TABLE users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100),
    email      VARCHAR(100) UNIQUE,
    password   VARCHAR(255),
    role       VARCHAR(50)  DEFAULT 'Student',
    phone      VARCHAR(20)  DEFAULT '',
    department VARCHAR(100) DEFAULT '',
    bio        TEXT         DEFAULT ''
);

CREATE TABLE leaves (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT,
    leave_type     VARCHAR(50),
    from_date      DATE,
    to_date        DATE,
    reason         TEXT,
    status         VARCHAR(20)  DEFAULT 'Pending',   -- final status
    faculty_name   VARCHAR(100) DEFAULT '',
    faculty_status VARCHAR(20)  DEFAULT 'Pending',   -- level 1
    faculty_remark TEXT         DEFAULT '',
    admin_status   VARCHAR(20)  DEFAULT 'Pending',   -- level 2
    admin_remark   TEXT         DEFAULT '',
    remarks        TEXT         DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

> All extra columns are added automatically on first run — no manual ALTER TABLE needed.

---

## Installation

**1. Clone the repo**

```bash
git clone https://github.com/pawanstar123/Smart-Leave-Management-System.git
cd Smart-Leave-Management-System
```

**2. Install dependencies**

```bash
pip install flask mysql-connector-python
```

**3. Update DB credentials in `app.py`**

```python
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="leave_system",
    auth_plugin='mysql_native_password'
)
```

**4. Run from the project root**

```bash
python app.py
```

Open `http://127.0.0.1:5000`

> Always run from the folder containing `templates/` and `static/`. Running from a subfolder causes `TemplateNotFound` errors.

---

## Routes

| Method | Route | Role | Description |
|--------|-------|------|-------------|
| GET | `/` | All | Landing page |
| GET/POST | `/register` | All | Register |
| GET/POST | `/login` | All | Login |
| GET | `/logout` | All | Logout |
| GET | `/user/dashboard` | Student | Dashboard with leave stats |
| GET/POST | `/user/apply_leave` | Student | Submit a leave request |
| GET | `/user/leave_history` | Student | Table with Faculty + Admin stage columns |
| GET | `/user/leave_status` | Student | Visual pipeline with both remarks |
| GET/POST | `/user/profile` | Student | Edit profile, change password |
| GET | `/faculty/dashboard` | Faculty | Pending count + quick review table |
| GET | `/faculty/leaves` | Faculty | All leaves — filter, search, remarks modal |
| POST | `/faculty/leave/<id>/approve` | Faculty | Approve → forwards to Admin |
| POST | `/faculty/leave/<id>/reject` | Faculty | Reject → final, Admin not involved |
| GET | `/admin/dashboard` | Admin | Stats, progress bars, recent pipeline view |
| GET | `/admin/users` | Admin | All users with search |
| GET | `/admin/leaves` | Admin | All leaves with Faculty + Admin columns |
| GET | `/admin/leaves?status=awaiting` | Admin | Only Faculty-approved, awaiting Admin |
| POST | `/admin/leave/<id>/approve` | Admin | Final approval |
| POST | `/admin/leave/<id>/reject` | Admin | Final rejection |

---

## User Roles

| Role | Level | Redirected To | Capabilities |
|------|-------|--------------|--------------|
| Student | — | `/user/dashboard` | Apply leave, track pipeline status with both remarks |
| Faculty | Level 1 | `/faculty/dashboard` | Review all leaves first — approve forwards to Admin, reject is final |
| Admin | Level 2 | `/admin/dashboard` | Final decision on Faculty-approved leaves only |

---

## Key Features

- Three-level approval pipeline — Student → Faculty → Admin with independent remarks at each stage
- Faculty rejection is final — Admin is not involved, student sees immediate result
- Admin only sees Faculty-approved leaves in the "Awaiting" view — clean separation of concerns
- Auto-reconnect DB helper (`q()`) — app stays up if MySQL connection drops
- Auto-migration on startup — all new columns added to existing tables automatically
- Visual approval pipeline on student's Leave Status page — shows each stage with badge + remark
- Awaiting-only filter on Admin leaves page — highlighted rows for quick action
- Live search + filter on all leave tables (client-side, no page reload)
- Remarks modal on Faculty and Admin pages — add remarks before confirming any decision
- Consistent dark-sidebar theme across all pages via a single shared CSS file

---
## ⚙️ How It Works

1. User registers and logs into the system
2. Based on role, user is redirected to respective dashboard
3. Students apply for leave
4. Faculty reviews and approves/rejects with remarks
5. Admin monitors overall system activity

## Notes

- Passwords are stored in plain text — hashing with `bcrypt` is strongly recommended before production
- Run `app.py` from the project root, not from any subfolder

---

## Contributors

| Name | Role |
|------|------|
| Pavan Agrawal | Developer |
| Keshav Kumar Singh | Developer |
| Rohan Kumar | Developer |
| Himanshu Kasana | Developer |
| Vipin | Developer |

Department of Computer Science (CSE-A), Faculty of Technology, University of Delhi

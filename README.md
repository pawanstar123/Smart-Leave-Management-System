# LeaveOk — Smart Leave Management System

A role-based leave management web app built with Flask and MySQL. Students apply for leaves, faculty review and approve/reject them with remarks, and admins oversee the entire system.

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
├── app.py                              # All Flask routes, DB logic, auto-reconnect
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
    │   ├── leave_history.html          # All leave requests table
    │   ├── leave_status.html           # Status with faculty name & remarks
    │   └── user_profile.html           # Tabbed profile — info, password, account
    │
    ├── faculty Dashboard/
    │   ├── Faculty_Dashboard.html      # Pending stats + quick approve/reject
    │   └── Faculty_Leave.html          # Full leave table with remarks modal
    │
    └── admin Dashboard/
        ├── admin_dashboard.html        # System stats + approval progress + recent leaves
        ├── admin_leaves.html           # Full leave table with approve/reject + filters
        └── admin_users.html            # All registered users with search
```

---

## Database Setup

Run this in your MySQL client:

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
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT,
    leave_type   VARCHAR(50),
    from_date    DATE,
    to_date      DATE,
    reason       TEXT,
    status       VARCHAR(20)  DEFAULT 'Pending',
    faculty_name VARCHAR(100) DEFAULT '',
    remarks      TEXT         DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

> The `phone`, `department`, `bio`, `faculty_name`, and `remarks` columns are added automatically on first run if they don't exist.

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
cd "D:\path\to\Smart-Leave-Management-System"
python app.py
```

Then open `http://127.0.0.1:5000`

> Make sure you run `app.py` from the folder that contains the `templates/` and `static/` directories, not from a subfolder.

---

## Routes

| Method | Route | Role | Description |
|--------|-------|------|-------------|
| GET | `/` | All | Landing page |
| GET/POST | `/register` | All | Register new user |
| GET/POST | `/login` | All | Login |
| GET | `/logout` | All | Logout |
| GET | `/user/dashboard` | Student | Dashboard with leave stats |
| GET/POST | `/user/apply_leave` | Student | Submit a leave request |
| GET | `/user/leave_history` | Student | View all personal leave requests |
| GET | `/user/leave_status` | Student | Status with faculty name & remarks |
| GET/POST | `/user/profile` | Student | Edit profile, change password |
| GET | `/faculty/dashboard` | Faculty | Pending leaves overview + quick actions |
| GET | `/faculty/leaves` | Faculty | All leaves with search, filter, remarks modal |
| POST | `/faculty/leave/<id>/approve` | Faculty | Approve a leave with remarks |
| POST | `/faculty/leave/<id>/reject` | Faculty | Reject a leave with remarks |
| GET | `/admin/dashboard` | Admin | System stats + approval progress + recent requests |
| GET | `/admin/users` | Admin | All registered users with search |
| GET | `/admin/leaves` | Admin | All leave requests with filters |
| POST | `/admin/leave/<id>/approve` | Admin | Approve a leave |
| POST | `/admin/leave/<id>/reject` | Admin | Reject a leave |

---

## User Roles

| Role | Redirected To | Capabilities |
|------|--------------|--------------|
| Student | `/user/dashboard` | Apply leave, view history/status, manage profile |
| Faculty | `/faculty/dashboard` | Review all leaves, approve/reject with remarks |
| Admin | `/admin/dashboard` | View all users, approve/reject all leaves, system overview |

---

## Features

- Role-based login — auto-redirects to the correct dashboard on sign-in
- Auto-reconnect DB helper (`q()`) — app stays up even if MySQL connection drops
- Auto-migration — missing columns added to DB on first run, no manual SQL needed
- User dashboard with live leave stats (Total / Approved / Pending / Rejected)
- Faculty dashboard with pending count badge in sidebar, remarks modal for approve/reject
- Admin dashboard with approval progress bars and recent leave activity
- Live search and status/type filters on all leave tables (client-side, no page reload)
- Professional profile page — tabbed layout with personal info, password change, account details
- Consistent dark-sidebar theme across all pages via a single shared CSS file

---
## ⚙️ How It Works

1. User registers and logs into the system
2. Based on role, user is redirected to respective dashboard
3. Students apply for leave
4. Faculty reviews and approves/rejects with remarks
5. Admin monitors overall system activity

## Notes

- Passwords are stored in plain text — hashing with `bcrypt` is strongly recommended before any production use
- Run `app.py` from the project root directory, not from any subfolder, or Flask won't find the `templates/` folder

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

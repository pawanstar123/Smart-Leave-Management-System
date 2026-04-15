# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "smart_leave_secret_key"

db = None
cursor = None

def connect_db():
    global db, cursor
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pavan@985",
        database="leave_system",
        auth_plugin='mysql_native_password'
    )
    cursor = db.cursor()

def q(sql, vals=None):
    global db, cursor
    try:
        if db is None or not db.is_connected():
            connect_db()
        cursor.execute(sql, vals) if vals else cursor.execute(sql)
    except mysql.connector.errors.OperationalError:
        connect_db()
        cursor.execute(sql, vals) if vals else cursor.execute(sql)

def commit():
    db.commit()

# ── Startup: connect + migrate ────────────────────────────────────────────────
try:
    connect_db()
    print("MySQL Connected")

    # users columns
    for col, defn in [
        ("phone",      "VARCHAR(20) DEFAULT ''"),
        ("department", "VARCHAR(100) DEFAULT ''"),
        ("bio",        "TEXT DEFAULT ''"),
    ]:
        try:
            q(f"ALTER TABLE users ADD COLUMN {col} {defn}")
            commit()
        except Exception:
            pass

    # leaves columns — three-level approval
    for col, defn in [
        ("faculty_name",   "VARCHAR(100) DEFAULT ''"),
        ("faculty_status", "VARCHAR(20)  DEFAULT 'Pending'"),
        ("faculty_remark", "TEXT DEFAULT ''"),
        ("admin_status",   "VARCHAR(20)  DEFAULT 'Pending'"),
        ("admin_remark",   "TEXT DEFAULT ''"),
        ("remarks",        "TEXT DEFAULT ''"),
    ]:
        try:
            q(f"ALTER TABLE leaves ADD COLUMN {col} {defn}")
            commit()
        except Exception:
            pass

except Exception as e:
    print("MySQL Error:", e)


# ── Home ──────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template("home.html")

# ── Register ──────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role     = request.form.get('role', 'Student')

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")
        try:
            q("INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
              (name, email, password, role))
            commit()
        except mysql.connector.errors.IntegrityError:
            return render_template("register.html", error="Email already registered.")
        return redirect('/login')

    return render_template("register.html")

# ── Login ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        q("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id']    = user[0]
            session['user_name']  = user[1]
            session['user_email'] = user[2]
            # role column — handle created_at being present at index 5
            session['role'] = user[4] if len(user) > 4 else 'Student'

            role = session['role']
            if role == 'Admin':
                return redirect('/admin/dashboard')
            elif role == 'Faculty':
                return redirect('/faculty/dashboard')
            else:
                return redirect('/user/dashboard')
        else:
            return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")

# ── Logout ────────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ══════════════════════════════════════════════════════════════════════════════
# USER ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    uid = session['user_id']
    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s", (uid,))
    total = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s AND status='Approved'", (uid,))
    approved = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s AND status='Pending'", (uid,))
    pending = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s AND status='Rejected'", (uid,))
    rejected = cursor.fetchone()[0]

    return render_template(
        'user Dashboard/user_dashboard.html',
        user_name=session.get('user_name'),
        total_leaves=total, approved_leaves=approved,
        pending_leaves=pending, rejected_leaves=rejected
    )

@app.route('/user/apply_leave', methods=['GET', 'POST'])
def apply_leave():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        uid = session['user_id']
        q("""INSERT INTO leaves
             (user_id, leave_type, from_date, to_date, reason,
              status, faculty_status, admin_status)
             VALUES (%s,%s,%s,%s,%s,'Pending','Pending','Pending')""",
          (uid, request.form['leave_type'], request.form['from_date'],
           request.form['to_date'], request.form['reason']))
        commit()
        return redirect('/user/leave_history')

    return render_template('user Dashboard/apply_leave.html')

@app.route('/user/leave_history')
def leave_history():
    if 'user_id' not in session:
        return redirect('/login')

    q("""SELECT id, leave_type, from_date, to_date,
                faculty_status, admin_status, status
         FROM leaves WHERE user_id=%s ORDER BY id DESC""",
      (session['user_id'],))
    return render_template('user Dashboard/leave_history.html', leaves=cursor.fetchall())

@app.route('/user/leave_status')
def leave_status():
    if 'user_id' not in session:
        return redirect('/login')

    q("""SELECT id, leave_type, from_date, to_date, status,
                faculty_name, faculty_status, faculty_remark,
                admin_status, admin_remark
         FROM leaves WHERE user_id=%s ORDER BY id DESC""",
      (session['user_id'],))
    return render_template('user Dashboard/leave_status.html',
                           leave_status_data=cursor.fetchall())

@app.route('/user/profile', methods=['GET', 'POST'])
def user_profile():
    if 'user_id' not in session:
        return redirect('/login')

    uid = session['user_id']

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_info':
            q("UPDATE users SET name=%s,email=%s,phone=%s,department=%s,bio=%s WHERE id=%s",
              (request.form['name'], request.form['email'],
               request.form.get('phone',''), request.form.get('department',''),
               request.form.get('bio',''), uid))
            commit()
            session['user_name']  = request.form['name']
            session['user_email'] = request.form['email']
        elif action == 'change_password':
            q("SELECT password FROM users WHERE id=%s", (uid,))
            row = cursor.fetchone()
            if row and row[0] == request.form['current_password']:
                if request.form['new_password'] == request.form['confirm_password']:
                    q("UPDATE users SET password=%s WHERE id=%s",
                      (request.form['new_password'], uid))
                    commit()
                    return redirect('/user/profile?pw=success')
                else:
                    return redirect('/user/profile?pw=mismatch')
            else:
                return redirect('/user/profile?pw=wrong')
        return redirect('/user/profile')

    try:
        q("SELECT id,name,email,role,phone,department,bio FROM users WHERE id=%s", (uid,))
        raw  = cursor.fetchone()
        user = (raw[0], raw[1], raw[2], raw[3], raw[4] or '', raw[5] or '', raw[6] or '') if raw else None
    except Exception:
        q("SELECT id,name,email,role FROM users WHERE id=%s", (uid,))
        raw  = cursor.fetchone()
        user = (raw[0], raw[1], raw[2], raw[3], '', '', '') if raw else None

    if not user:
        return redirect('/logout')

    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s", (uid,))
    total = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s AND status='Approved'", (uid,))
    approved = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE user_id=%s AND status='Pending'", (uid,))
    pending = cursor.fetchone()[0]

    return render_template(
        'user Dashboard/user_profile.html',
        user=user, total_leaves=total, approved_leaves=approved,
        pending_leaves=pending, pw_status=request.args.get('pw')
    )


# ══════════════════════════════════════════════════════════════════════════════
# FACULTY ROUTES  (Level 1 approval)
# ══════════════════════════════════════════════════════════════════════════════

def faculty_required():
    return 'user_id' in session and session.get('role') == 'Faculty'

@app.route('/faculty/dashboard')
def faculty_dashboard():
    if not faculty_required():
        return redirect('/login')

    # Faculty sees only leaves awaiting their review
    q("SELECT COUNT(*) FROM leaves WHERE faculty_status='Pending'")
    pending = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE faculty_status='Approved'")
    approved = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE faculty_status='Rejected'")
    rejected = cursor.fetchone()[0]

    q("""SELECT l.id, u.name, l.leave_type, l.from_date, l.to_date, l.faculty_status
         FROM leaves l JOIN users u ON l.user_id = u.id
         WHERE l.faculty_status = 'Pending' ORDER BY l.id DESC LIMIT 10""")
    pending_leaves = cursor.fetchall()

    return render_template(
        'faculty Dashboard/Faculty_Dashboard.html',
        faculty_name=session.get('user_name'),
        pending=pending, approved=approved, rejected=rejected,
        pending_leaves=pending_leaves
    )

@app.route('/faculty/leaves')
def faculty_leaves():
    if not faculty_required():
        return redirect('/login')

    status_filter = request.args.get('status', '')
    if status_filter:
        q("""SELECT l.id, u.name, l.leave_type, l.from_date, l.to_date,
                    l.reason, l.faculty_status, l.faculty_remark
             FROM leaves l JOIN users u ON l.user_id = u.id
             WHERE l.faculty_status = %s ORDER BY l.id DESC""", (status_filter,))
    else:
        q("""SELECT l.id, u.name, l.leave_type, l.from_date, l.to_date,
                    l.reason, l.faculty_status, l.faculty_remark
             FROM leaves l JOIN users u ON l.user_id = u.id ORDER BY l.id DESC""")

    return render_template('faculty Dashboard/Faculty_Leave.html',
                           leaves=cursor.fetchall(), status_filter=status_filter)

@app.route('/faculty/leave/<int:leave_id>/approve', methods=['POST'])
def faculty_approve_leave(leave_id):
    if not faculty_required():
        return redirect('/login')
    remark       = request.form.get('remarks', '')
    faculty_name = session.get('user_name')
    # Faculty approves → forward to Admin (status stays Pending until Admin acts)
    q("""UPDATE leaves
         SET faculty_status='Approved', faculty_name=%s, faculty_remark=%s,
             status='Pending'
         WHERE id=%s""", (faculty_name, remark, leave_id))
    commit()
    return redirect('/faculty/leaves')

@app.route('/faculty/leave/<int:leave_id>/reject', methods=['POST'])
def faculty_reject_leave(leave_id):
    if not faculty_required():
        return redirect('/login')
    remark       = request.form.get('remarks', '')
    faculty_name = session.get('user_name')
    # Faculty rejects → final rejection, no need for Admin
    q("""UPDATE leaves
         SET faculty_status='Rejected', faculty_name=%s, faculty_remark=%s,
             admin_status='N/A', status='Rejected'
         WHERE id=%s""", (faculty_name, remark, leave_id))
    commit()
    return redirect('/faculty/leaves')


# ══════════════════════════════════════════════════════════════════════════════
# ADMIN ROUTES  (Level 2 approval — only Faculty-approved leaves)
# ══════════════════════════════════════════════════════════════════════════════

def admin_required():
    return 'user_id' in session and session.get('role') == 'Admin'

@app.route('/admin/dashboard')
def admin_dashboard():
    if not admin_required():
        return redirect('/login')

    q("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves")
    total_leaves = cursor.fetchone()[0]
    # Awaiting Admin = Faculty approved but Admin not yet acted
    q("SELECT COUNT(*) FROM leaves WHERE faculty_status='Approved' AND admin_status='Pending'")
    pending_leaves = cursor.fetchone()[0]
    q("SELECT COUNT(*) FROM leaves WHERE status='Approved'")
    approved_leaves = cursor.fetchone()[0]

    q("""SELECT l.id, u.name, l.leave_type, l.from_date, l.to_date,
                l.faculty_status, l.admin_status, l.status
         FROM leaves l JOIN users u ON l.user_id = u.id
         ORDER BY l.id DESC LIMIT 10""")
    recent_leaves = cursor.fetchall()

    return render_template(
        'admin Dashboard/admin_dashboard.html',
        total_users=total_users, total_leaves=total_leaves,
        pending_leaves=pending_leaves, approved_leaves=approved_leaves,
        recent_leaves=recent_leaves
    )

@app.route('/admin/users')
def admin_users():
    if not admin_required():
        return redirect('/login')
    q("SELECT id,name,email,role FROM users ORDER BY id DESC")
    return render_template('admin Dashboard/admin_users.html', users=cursor.fetchall())

@app.route('/admin/leaves')
def admin_leaves():
    if not admin_required():
        return redirect('/login')

    status_filter = request.args.get('status', '')
    if status_filter == 'awaiting':
        q("""SELECT l.id, u.name, l.leave_type, l.from_date, l.to_date, l.reason,
                    l.faculty_status, l.faculty_remark, l.admin_status, l.status
             FROM leaves l JOIN users u ON l.user_id = u.id
             WHERE l.faculty_status='Approved' AND l.admin_status='Pending'
             ORDER BY l.id DESC""")
    else:
        q("""SELECT l.id, u.name, l.leave_type, l.from_date, l.to_date, l.reason,
                    l.faculty_status, l.faculty_remark, l.admin_status, l.status
             FROM leaves l JOIN users u ON l.user_id = u.id ORDER BY l.id DESC""")

    return render_template('admin Dashboard/admin_leaves.html',
                           leaves=cursor.fetchall(), status_filter=status_filter)

@app.route('/admin/leave/<int:leave_id>/approve', methods=['POST'])
def approve_leave(leave_id):
    if not admin_required():
        return redirect('/login')
    remark = request.form.get('remarks', '')
    q("""UPDATE leaves
         SET admin_status='Approved', admin_remark=%s, status='Approved'
         WHERE id=%s""", (remark, leave_id))
    commit()
    return redirect('/admin/leaves')

@app.route('/admin/leave/<int:leave_id>/reject', methods=['POST'])
def reject_leave(leave_id):
    if not admin_required():
        return redirect('/login')
    remark = request.form.get('remarks', '')
    q("""UPDATE leaves
         SET admin_status='Rejected', admin_remark=%s, status='Rejected'
         WHERE id=%s""", (remark, leave_id))
    commit()
    return redirect('/admin/leaves')


if __name__ == '__main__':
    app.run(debug=True)

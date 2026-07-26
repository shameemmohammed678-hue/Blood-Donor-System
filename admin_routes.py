from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash,generate_password_hash
from database.db_connection import get_connection
import pymysql

admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates",
    url_prefix="/admin"
)


#admin login
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_connection()
        if conn is None:
            return "Database connection failed ",500
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM admin WHERE email=%s", (email,))
        admin = cursor.fetchone()
        conn.close()

        
        if admin and check_password_hash(admin["password"], password):
                session["admin_id"] = admin["admin_id"]
                session["role"] = admin["role"] 
                return redirect(url_for("admin.admin_dashboard"))


        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")



# admin dashboard
@admin_bp.route("/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))
    return render_template("admin_dashboard.html",role = session.get("role"))


# admin viwe Donors
@admin_bp.route("/donors")
def view_donors():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT donor_id, D_name AS d_name, email, phone, blood_group, location FROM donor")
    donors = cursor.fetchall()
    conn.close()

    return render_template("admin_view_donor.html", donors=donors)


# admin delete donors
@admin_bp.route("/delete_donor/<int:donor_id>")
def delete_donor(donor_id):
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM emergency_request WHERE donor_id =%s", (donor_id,))
    result = cursor.fetchone()
    count = result["total"]
    
    if count > 0:
        conn.close()
        flash("Cannot Delete Donor: Donor has emergency requests.","danger")
        return redirect(url_for("admin.view_donors"))
    
    cursor.execute("DELETE  FROM donor WHERE donor_id = %s",(donor_id,))
    conn.commit()
    conn.close()
    flash("Donor Deleted Successfully","success")
    return redirect(url_for("admin.view_donors"))

# admin view hospitals
@admin_bp.route("/hospitals")
def view_hospitals():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT hospital_id, H_name, email, phone, address FROM hospital")
    hospitals = cursor.fetchall()
    conn.close()

    return render_template("admin_view_hospital.html", hospitals=hospitals)


#admin delete hospital
@admin_bp.route("/delete_hospital/<int:hospital_id>")
def delete_hospital(hospital_id):
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM emergency_request WHERE hospital_id =%s", (hospital_id,))
    result = cursor.fetchone()
    count = result["total"]
    if count >0:
        conn.close()
        flash("Cannot Delete Hospital: Hospital has Emergency Request","danger")
        return redirect(url_for("admin.view_hospitals"))


    cursor.execute("DELETE FROM hospital WHERE hospital_id = %s",(hospital_id,))
    conn.commit()
    conn.close()
    flash("Hospital removed successfully")
    return redirect(url_for("admin.view_hospitals"))



#  admin view request
@admin_bp.route("/requests")
def view_requests():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT r.request_id, h.H_name, d.D_name, r.required_blood_group, r.status
        FROM emergency_request r
        JOIN hospital h ON r.hospital_id = h.hospital_id
        JOIN donor d ON r.donor_id = d.donor_id
    """)
    requests = cursor.fetchall()
    conn.close()

    return render_template("admin_view_request.html", requests=requests)



@admin_bp.route("/create_admin", methods=["GET", "POST"])
def create_admin():

    # Must be logged in
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    # Only super_admin can create admin
    if session.get("role") != "super_admin":
        return "Access Denied"

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO admin (email, password, role) VALUES (%s, %s, %s)",
            (email, hashed_password, "admin")
        )

        conn.commit()
        conn.close()

        flash("New Admin Created Successfully", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("create_admin.html")

# View Admins
@admin_bp.route("/view_admins")
def view_admins():
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    # Only super admin can view admins
    if session.get("role") != "super_admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT admin_id, email, role FROM admin")
    admins = cursor.fetchall()

    conn.close()

    return render_template("view_admins.html", admins=admins)


# Delete Admin
@admin_bp.route("/delete_admin/<int:admin_id>")
def delete_admin(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("admin.admin_login"))

    # Only super admin can delete
    if session.get("role") != "super_admin":
        flash("Access Denied!", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    # Prevent deleting yourself
    if admin_id == session.get("admin_id"):
        flash("You cannot delete yourself!", "warning")
        return redirect(url_for("admin.view_admins"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM admin WHERE admin_id = %s", (admin_id,))
    conn.commit()
    conn.close()

    flash("Admin deleted successfully!", "success")
    return redirect(url_for("admin.view_admins"))




#admin logout 
@admin_bp.route("/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin.admin_login"))

from flask import Blueprint, request, jsonify,render_template,session,redirect,url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import get_connection

donor_bp = Blueprint('donor', __name__, url_prefix='/donor')

@donor_bp.route('/home')
def donor_home():
    return render_template("donor_dashboard.html",donor_name = session.get("donor_name"),donor_id = session.get("donor_id"))


@donor_bp.route('/register_page')
def donor_register_page():
    return render_template("donor_registration.html",donor_id = session.get("donor_id"))



@donor_bp.route('/login_page')
def donor_login_page():
    return render_template("donor_login.html")



@donor_bp.route('/view_request_page')
def donor_view_request_page():
    return render_template("donor_viewrequestpage.html",donor_id = session.get("donor_id"))




@donor_bp.route('/update_page')
def donor_update_page():
    return render_template("donor_update.html")

@donor_bp.route('/logout')
def donor_logout():
    session.clear()
    return redirect(url_for('donor.donor_login_page'))


#donor registration
@donor_bp.route('/register', methods=['POST'])
def register_donor():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    age = data.get("age")
    try:
        age = int(age)
    except(TypeError,ValueError):
        return jsonify({"error":"Age must be a valid number"}),400
    if age <18 or age>60:
        return jsonify({"error":"Only Donors between 18 and 60 years are eligible to Donate Blood"}),400
    gender = data.get("gender")
    blood_group = data.get("blood_group")
    location = data.get("location")
    address = data.get("address")

    if not (name and email and password and phone):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO donor 
            (D_Name, age, gender, blood_group, phone, email, password, address, location, availability_status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            values = (name,age,gender,blood_group,phone,email,hashed_password,address,location,"Available")

            cursor.execute(sql, values)
            conn.commit()

        return jsonify({"message": "Donor registered successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()




#donor login
@donor_bp.route('/login', methods=['GET','POST'])
def donor_login():
    if request.method == "GET":
        return render_template("donor_login.html")
    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM donor WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

            if user is None:
                return jsonify({"error": "Email not found"}), 404

            if check_password_hash(user["password"], password):
                session["donor_id"] = user["donor_id"]
                session["donor_name"] = user["D_Name"]
                return jsonify({
                    "message": "Login successful!",
                    "donor_id": user["donor_id"],
                    "name": user["D_Name"]
                }), 200

            return jsonify({"error": "Invalid password"}), 401

    finally:
        conn.close()

# update availability of donor
@donor_bp.route('/update_availability', methods=['POST'])
def update_availability():
    data = request.json

    donor_id = session.get('donor_id')
    status = data.get('status')  

    if status not in ["Available", "Not Available"]:
        return jsonify({"error": "Invalid status"}), 400

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE donor 
            SET availability_status = %s 
            WHERE donor_id = %s
            """
            cursor.execute(sql, (status, donor_id))
            conn.commit()

        return jsonify({"message": "Availability updated successfully"}), 200

    finally:
        conn.close()

# donor view requests
@donor_bp.route('/view_requests', methods=['POST'])
def view_requests():
    try:
        data = request.json
        donor_id = data.get("donor_id")

        if not donor_id:
            return jsonify({"error": "Missing donor_id"}), 400

        conn = get_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        with conn.cursor(pymysql.cursors.DictCursor) as cursor:   # IMPORTANT!
            sql = """
                SELECT 
                    er.request_id,
                    er.required_blood_group,
                    er.request_message,
                    er.status,
                    er.created_at,
                    h.H_Name AS hospital_name,
                    h.phone AS hospital_phone
                FROM emergency_request er
                LEFT JOIN hospital h ON er.hospital_id = h.hospital_id
                WHERE er.donor_id = %s
                ORDER BY er.created_at DESC
            """
            cursor.execute(sql, (donor_id,))
            results = cursor.fetchall()

        conn.close()
        return jsonify({"requests": results}), 200

    except Exception as e:
        print("ERROR IN /view_requests:", e)
        return jsonify({"error": str(e)}), 500

@donor_bp.route('/respond_request', methods=['POST'])
def respond_request():
    data = request.json
    request_id = data.get("request_id")
    response = data.get("response")  # "Accepted" or "Rejected"

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database error"}), 500

    try:
        with conn.cursor() as cursor:
            sql = "UPDATE emergency_request SET status = %s WHERE request_id = %s"
            cursor.execute(sql, (response, request_id))
            conn.commit()

        return jsonify({"message": f"Request {response} successfully!"}), 200

    finally:
        conn.close()

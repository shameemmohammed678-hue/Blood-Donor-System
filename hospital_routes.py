from flask import Blueprint, request, jsonify,render_template,session,redirect,url_for
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import get_connection
from twilio.rest import Client
from twilio_config import ACCOUNT_SID,AUTH_TOKEN,TWILIO_PHONE
from datetime import datetime,timedelta

hospital_bp = Blueprint('hospital', __name__, url_prefix='/hospital')

@hospital_bp.route('/register_page')
def hospital_register_page():
    return render_template("hospital_register.html")

@hospital_bp.route('/login_page')
def hospital_login_page():
    return render_template("hospital_login.html")

@hospital_bp.route('/dashboard_page')
def hospital_dashboard_page():
    return render_template("hospital_dashboard.html")

@hospital_bp.route('/search_page')
def hospital_search_page():
    return render_template("hospital_search.html")

@hospital_bp.route('/view_status_page')
def hospital_view_page():
    return render_template("hospital_view_status.html")

@hospital_bp.route('/emergency_request_page')
def emergency_request_page():
    return render_template("hospital_emergency_request.html")

@hospital_bp.route('/logout')
def hospital_logout():
    session.clear()
    return redirect(url_for('hospital.hospital_login_page'))

@hospital_bp.route('/register', methods=['POST'])
def register_hospital():
    data = request.json

    name = data.get('hospital_name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    address = data.get('address')

    if not (name and email and password and phone and address):
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO hospital (H_Name, email, password, address, phone)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, hashed_password, address, phone))
            conn.commit()

        return jsonify({"message": "Hospital Registered Successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        conn.close()




@hospital_bp.route('/login', methods=['GET','POST'])
def hospital_login():
    if request.method == 'GET':
        return render_template("hospital_login.html")
    data = request.json

    email = data.get('email')
    password = data.get('password')

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM hospital WHERE email = %s"
            cursor.execute(sql, (email,))
            hospital = cursor.fetchone()

            if hospital is None:
                return jsonify({"error": "Email not found"}), 404

            if check_password_hash(hospital["password"], password):
                session["hospital_id"] = hospital["hospital_id"]
                
                return jsonify({
                    "message": "Login Successful",
                    "hospital_id": hospital["hospital_id"],
                    "name": hospital["H_name"]
                })
            else:
                return jsonify({"error": "Invalid password"}), 401

    finally:
        conn.close()




@hospital_bp.route('/search', methods=['POST'])
def search_donors():
    data = request.json
    blood_group = data.get("blood_group")
    location = data.get("location")

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database error"}), 500

    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT donor_id, D_Name, phone, email, blood_group, location, availability_status
            FROM donor
            WHERE blood_group = %s AND location = %s 
            """
            cursor.execute(sql, (blood_group, location))
            result = cursor.fetchall()

        return jsonify({"donors": result}), 200

    finally:
        conn.close()



@hospital_bp.route('/send_request', methods=['POST'])
def send_emergency_request():
    data = request.json

    hospital_id = session.get("hospital_id")
    donor_id = data.get("donor_id")
    required_blood_group = data.get("required_blood_group")
    message = data.get("message")

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database error"}), 500

    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO emergency_request (donor_id, hospital_id, required_blood_group, request_message)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (donor_id, hospital_id, required_blood_group, message))
            conn.commit()
            cursor.execute("""SELECT phone FROM donor WHERE donor_id = %s""",(donor_id,))
            donor = cursor.fetchone()
            if donor:
                donor_phone = donor['phone']
                sms = ("Emergency Blood Request! \n"
                       f"Required Blood Group:{required_blood_group}\n"
                       "Hospital needs Blood Urgently.\n"
                       "open Blood Donation App to respond."
                       )
                client = Client(ACCOUNT_SID,AUTH_TOKEN)
                client.messages.create(
                    body=sms,
                    from_= TWILIO_PHONE,
                    to = donor_phone
                )
        return jsonify({"message": "Emergency Request Sent & sms Notified"}), 201
    except Exception as e:
        return jsonify({"message":"Emergency Request sent, but sms notification failed","error":str(e)}),201

    finally:
        conn.close()



@hospital_bp.route('/view_status', methods=['POST'])
def view_status():

    hospital_id = session.get("hospital_id")
    if not hospital_id:
        return jsonify({"error": "Not authenticated (hospital_id missing)"}), 401

    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # use a dictionary cursor so we return JSON-friendly dicts
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
            SELECT
                er.request_id,
                d.D_Name AS donor_name,
                d.blood_group,
                er.status,
                er.created_at,
                d.phone AS donor_phone
            FROM emergency_request er
            LEFT JOIN donor d ON er.donor_id = d.donor_id
            WHERE er.hospital_id = %s
            ORDER BY er.created_at DESC
            """
            cursor.execute(sql, (hospital_id,))
            results = cursor.fetchall()
    except Exception as e:
        # log the exception server-side (print or logger)
        print("view_status error:", e)
        return jsonify({"error": "Server error retrieving requests"}), 500
    finally:
        try:
            conn.close()
        except:
            pass

    return jsonify({"requests": results}), 200
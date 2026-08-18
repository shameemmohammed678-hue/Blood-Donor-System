# 🩸 Blood Donor Finder and Emergency Request System

A full-stack web application designed to help hospitals quickly find suitable blood donors and send emergency blood requests during critical situations.

## 📌 Project Overview

The **Blood Donor Finder and Emergency Request System** connects donors, hospitals, and administrators through a centralized web platform. Hospitals can search for donors based on blood group and send emergency requests, while donors can manage their profiles and receive notifications.

The application is built with **Python Flask**, uses **TiDB Cloud (MySQL-compatible)** for cloud database storage, and integrates the **Twilio SMS API** for donor notifications.

## ✨ Features

### 🩸 Donor

* Donor registration and login
* Manage donor profile
* Search and view requests
* Receive emergency request notifications

### 🏥 Hospital

* Hospital registration and login
* Hospital dashboard
* Search donors by blood group
* Send emergency blood requests
* View request status

### 👨‍💼 Admin

* Admin authentication
* Manage donors
* Manage hospitals
* Manage administrators
* Monitor emergency requests

### 📱 Notifications

* SMS notifications using Twilio API

### 🔐 Security

* Password hashing
* Session management
* Role-based access control
* Input validation
* Environment-based configuration for sensitive credentials

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Backend

* Python
* Flask

### Database

* MySQL
* TiDB Cloud
* PyMySQL

### APIs & Services

* Twilio SMS API

### Deployment & Tools

* Vercel
* Git
* GitHub

---

## 🔄 System Workflow

```text
Donor Registration
        ↓
Donor Profile
        ↓
Hospital Searches Donors
        ↓
Hospital Sends Emergency Request
        ↓
Request Stored in Cloud Database
        ↓
Twilio SMS Notification
        ↓
Donor Receives Emergency Request
```

---

## 📁 Project Structure

```text
Blood-Donor-System/
│
├── api/
│   └── index.py
│
├── certs/
│   └── isrgrootx1.pem
│
├── database/
│   └── db_connection.py
│
├── routes/
│   ├── admin_routes.py
│   ├── donor_routes.py
│   └── hospital_routes.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── donor/
│   ├── hospital/
│   └── admin/
│
├── app.py
├── config.py
├── requirements.txt
├── twilio_config.py
├── vercel.json
├── .env
└── README.md
```

> **Note:** `.env` contains sensitive credentials and should not be committed to GitHub.

---

## ⚙️ Environment Variables

Create a `.env` file in the project root and configure the required environment variables:

```env
SECRET_KEY=your_secret_key

MYSQL_HOST=your_database_host
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_database_password
MYSQL_DB=your_database_name

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

Keep all credentials private and never expose them publicly.

---

## 🚀 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/shameemmohammed678-hue/Blood-Donor-System.git
```

### 2. Navigate to the project directory

```bash
cd Blood-Donor-System
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file and add the required database, Flask, and Twilio credentials.

### 6. Run the application

```bash
python app.py
```

### 7. Open in your browser

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

The application uses:

* **Vercel** — Application deployment
* **TiDB Cloud** — Cloud-hosted MySQL-compatible database
* **GitHub** — Source code and version control
* **Twilio** — SMS notification service

Environment variables are configured separately in the deployment platform rather than storing sensitive credentials in the source code.

---

## 🔒 Security Practices

* Passwords are securely hashed before storage.
* Sensitive credentials are stored using environment variables.
* Database communication uses SSL.
* Role-based access control restricts administrative functionality.
* User input is validated before processing.
* `.env` files are excluded from version control.

---

## 🔮 Future Enhancements

* Forgot password and password recovery
* Email notification system
* GPS/location-based donor search
* Advanced donor availability filtering
* Mobile application
* Real-time request status updates

---

## 👨‍💻 Developed By

**Mohammed Shameem J**

---

## 📚 Technologies & Documentation

* Flask
* MySQL / TiDB Cloud
* PyMySQL
* Twilio API
* Vercel
* HTML, CSS & JavaScript
* Git & GitHub

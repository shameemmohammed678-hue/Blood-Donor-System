from flask import Flask,render_template
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from routes.donor_routes import donor_bp
    app.register_blueprint(donor_bp)

    from routes.hospital_routes import hospital_bp
    app.register_blueprint(hospital_bp)

    from routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    @app.route('/')
    def home():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1",port=5000,debug=True)
 
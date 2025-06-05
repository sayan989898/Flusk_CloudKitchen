from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime
from models import db, User
from config import Config

# Flask app initialization
app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Load user callback for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Registration page (Customer only)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        hashed_pw = hashlib.md5(password.encode()).hexdigest()

        new_user = User(username=username, email=email, phone=phone, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")


# Login for all users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password_input):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            if user.user_type == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.user_type == 'delivery':
                return redirect(url_for('delivery_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))
        else:
            flash('Login failed. Check your credentials.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Admin Dashboard
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.user_type != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

# Customer Dashboard
@app.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if current_user.user_type != 'customer':
        return redirect(url_for('login'))
    return render_template('customer_dashboard.html')

# Delivery Partner Dashboard
@app.route('/delivery/dashboard')
@login_required
def delivery_dashboard():
    if current_user.user_type != 'delivery':
        return redirect(url_for('login'))
    return render_template('delivery_dashboard.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

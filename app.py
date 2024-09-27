from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import subprocess
import os
import time
import threading

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hooks.db'  # SQLite database for simplicity
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

db = SQLAlchemy(app)
mail = Mail(app)

# Database model to store hook alerts
class HookAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    syscall_number = db.Column(db.String(10), nullable=False)
    message = db.Column(db.String(200), nullable=False)

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Route to display hooks
@app.route('/hooks')
def hooks():
    alerts = HookAlert.query.all()
    return render_template('hooks.html', alerts=alerts)

# Route to send email alerts
@app.route('/send_alert/<syscall_number>', methods=['POST'])
def send_alert(syscall_number):
    try:
        # Prepare email
        msg = Message('Hook Detected!', sender=os.getenv('EMAIL_USER'), recipients=[os.getenv('MAIL_RECIPIENT')])
        msg.body = f"Hook detected in syscall table: {syscall_number}"
        mail.send(msg)

        # Log to database
        new_alert = HookAlert(syscall_number=syscall_number, message="Hook detected and email sent.")
        db.session.add(new_alert)
        db.session.commit()

        flash('Alert sent and logged!', 'success')
    except Exception as e:
        flash(f'Failed to send alert: {str(e)}', 'danger')
    
    return redirect(url_for('hooks'))

# Function to check for hooks
def monitor_hooks():
    while True:
        # Replace this with your logic to check for hooks from the kernel module
        # For example, you could read a log file or use a custom IPC method to detect hooks
        # Here we simulate the detection of a hook for demonstration
        time.sleep(5)  # Check every 5 seconds (adjust as necessary)

        # Simulate detected syscall number for testing
        syscall_number = '5'  # Replace with the actual detected syscall number
        send_alert(syscall_number)  # Send alert for demo

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    threading.Thread(target=monitor_hooks, daemon=True).start()  # Start monitoring in a separate thread
    flash('Monitoring started!', 'info')
    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()  # Create database tables
    app.run(debug=True)  # Run Flask application

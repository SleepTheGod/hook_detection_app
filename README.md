# Run the Application
Install Required Packages
Make sure to install Flask and other dependencies
```bash
pip install -r requirements.txt
```
# Set Environment Variables
Set the necessary environment variables for email credentials and recipient email
```bash
export EMAIL_USER='your_email@gmail.com'
export EMAIL_PASS='your_email_password'
export MAIL_RECIPIENT='recipient_email@gmail.com'
```
# Run the Flask Application
Start the Flask app
```bash
python app.py
```
# NOTE
Monitor Hooks
Click the "Start Monitoring" button on the home page to begin monitoring. This will simulate hook detection every 5 seconds and send email alerts for demonstration purposes.
Final Adjustments
Kernel Module Integration: You'll need to implement the logic to interact with your kernel module directly. This can be done via reading files, IPC, or custom syscalls as needed.
Testing and Debugging: Ensure that the email functionality works correctly and that the database logs alerts as expected.
Deployment: For a production environment, consider deploying the Flask application with a proper WSGI server and secure your email credentials.

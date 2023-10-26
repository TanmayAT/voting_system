from flask import Flask, render_template, request, redirect, url_for, flash, session , make_response
import smtplib
from email.mime.text import MIMEText
import random 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://root:@localhost/votingsystem'  # SQLite URI
db = SQLAlchemy(app)

class votongdata(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone_no = db.Column(db.String(120), unique=True, nullable=False)
    coordinates = db.Column(db.String(120), unique=True, nullable=False) 
   

class otp(db.Model) :
    phone_no = db.Column(db.String(120), unique=True, nullable=False)
    
    otp = db.Column(db.String(120), unique=True, nullable=False)
    
class team(db.Model) :
    phone_no = db.Column(db.String(120), unique=True, nullable=False)
    
    team_name = db.Column(db.String(120), unique=True, nullable=False)
    
    team_rank = db.Column(db.String(120), unique=True, nullable=False)
    


# Configure your email settings

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'tecnocracy.nitrr@gmail.com'
SMTP_PASSWORD = 'jnca hltp hfuk yutb'

@app.route('/set_cookie', methods=['GET'])
def set_cookie():
    # You can set the cookie here.
    response = make_response('Cookie set successfully')
    response.set_cookie('my_cookie', 'cookie_value', max_age=3600)  # Example cookie with a 1-hour lifetime
    return response
    

@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    my_cookie = request.cookies.get('my_cookie')
    return f'Value of "my_cookie" is: {my_cookie}'

@app.route('/send_verification_email')
def send_verification_email():
    try:
        recipient_email = 'vaidikpandeytt@gmail.com'  
        otp =  "".join([str(random.randint(0,9)) for i in range(4)]) 
        subject = 'Email Confirmation'
        message = f'OTP to confirm your email: {otp}'
        otp_record = otp(phone_no = phone_no  , otp=otp)
        db.session.add(otp_record)
        db.session.commit()

        # Email Formation 
        
        
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = SMTP_USERNAME
        msg['To'] = recipient_email

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipient_email, msg.as_string())
        server.quit()

        flash('Verification email sent!', 'success')
        
    except Exception as e:
        
        flash(f'Error sending verification email: {str(e)}', 'error')

    return redirect(url_for('index'))


@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        email = request.form['email']
        user_otp = request.form['otp']

        # Query the database for the stored OTP associated with the provided email
        stored_otp_record = otp.query.filter_by(phone_no=email).first()

        if stored_otp_record and stored_otp_record.otp == user_otp:
            # OTP matches; mark the user as verified in your database
            # You can set a flag in the user's record or perform any other necessary action
            flash('Email verified successfully!', 'success')
        else:
            flash('Invalid OTP. Please try again.', 'error')

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

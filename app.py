from flask import Flask, session, request, jsonify, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        try:
            contact_data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'message': request.form.get('message')
            }

            if not all(contact_data.values()):
                flash('All fields are required!', 'error')
                return redirect(url_for('home'))

            msg = Message(
                'New Contact Form Submission - RevuteAI',
                recipients=[os.getenv('NOTIFICATION_EMAIL')]
            )
            msg.body = f"""
New Contact Form Submission:
Name: {contact_data['name']}
Email: {contact_data['email']}
Phone: {contact_data['phone']}
Message: {contact_data['message']}
            """

            mail.send(msg)
            mongo.db.bfsi.insert_one(contact_data)
            flash('Thank you for contacting us!', 'success')

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error details:\n{error_details}")
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
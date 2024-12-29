from flask import Flask, session, request, jsonify, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Add a secret key for flash messages
app.secret_key = '123456789'  # Change this to a secure secret key

# MongoDB configuration
app.config[
    "MONGO_URI"] = "mongodb+srv://vasudha:vasudha@cluster0.0vkno.mongodb.net/bfsi?authSource=admin&retryWrites=true&w=majority&readPreference=primary"
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        try:
            # Get data from the form
            contact_data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'message': request.form.get('message')
            }

            # Validate required fields
            if not all(contact_data.values()):
                flash('All fields are required!', 'error')
                return redirect(url_for('home'))

            # Insert into database
            mongo.db.bfsi.insert_one(contact_data)

            flash('Thank you for contacting us! We will get back to you soon.', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            print(f"Error: {str(e)}")
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('home'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
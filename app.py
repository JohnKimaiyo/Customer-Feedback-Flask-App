from flask import Flask, request, render_template, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__)

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Path to the JSON file
DATA_FILE = 'data/feedback_data.json'

def load_feedback_data():
    """Load existing feedback data from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedback_data(data):
    """Save feedback data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET'])
def index():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    form_data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'county': request.form['county'],
        'email': request.form['email'],
        'product': request.form['product'],
        'rating': request.form['rating'],
        'comments': request.form['comments'],
        'date': request.form['date'],
        'phone': request.form['phone'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Add a timestamp
    }

    # Load existing feedback data
    feedback_data = load_feedback_data()

    # Append the new feedback to the existing data
    feedback_data.append(form_data)

    # Save the updated feedback data
    save_feedback_data(feedback_data)

    # Redirect to the confirmation page
    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
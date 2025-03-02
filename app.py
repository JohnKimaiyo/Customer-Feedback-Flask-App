from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)  # Ensure the data folder exists

@app.route('/')
def index():
    return render_template('feedback_form.html')  # Ensure this file is inside a 'templates' folder

@app.route('/submit', methods=['POST'])
def submit_feedback():
    data = request.json  # Receive JSON data from the frontend
    if not data or 'product' not in data or 'review' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    file_path = os.path.join(data_folder, "feedback.json")
    
    # Read existing data if available
    feedback_list = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                feedback_list = json.load(file)
            except json.JSONDecodeError:
                feedback_list = []
    
    # Append new feedback
    feedback_list.append(data)
    
    # Save back to JSON file
    with open(file_path, "w") as file:
        json.dump(feedback_list, file, indent=4)
    
    return jsonify({"message": "Feedback received", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True)

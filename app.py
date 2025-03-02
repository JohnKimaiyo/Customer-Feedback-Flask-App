from flask import Flask, render_template, request, jsonify
import json
import os
import pandas as pd

app = Flask(__name__)

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)  # Ensure the data folder exists

@app.route('/')
def home():
    return render_template('feedback_form.html')

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

# Adjust the path to the sentiment results JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "trained data", "sentiment_results.json")

# Load the dataset
try:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        reviews_data = json.load(file)
        reviews_df = pd.DataFrame(reviews_data)  # Convert JSON to Pandas DataFrame
except Exception as e:
    print(f"Error loading sentiment data: {e}")
    reviews_df = pd.DataFrame(columns=["product", "sentiment"])  # Initialize empty DataFrame

# Function to get sentiment for a product
def get_sentiment(product_name):
    filtered_reviews = reviews_df[reviews_df["product"].str.lower() == product_name.lower()]
    
    if filtered_reviews.empty:
        return {"error": "Product not found"}
    
    # Get the most common sentiment
    sentiment_counts = filtered_reviews["sentiment"].value_counts().to_dict()
    most_common_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    
    return {
        "product": product_name,
        "sentiment": most_common_sentiment,
        "sentiment_counts": sentiment_counts
    }

@app.route("/sentiment", methods=["GET", "POST"])
def sentiment():
    sentiment_data = None
    if request.method == "POST":
        product_name = request.form["product"]
        sentiment_data = get_sentiment(product_name)

    return render_template("sentiment_analysis.html", sentiment_data=sentiment_data)

if __name__ == "__main__":
    app.run(debug=True)
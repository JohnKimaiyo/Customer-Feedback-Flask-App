#!/usr/bin/env python
# coding: utf-8

# # Customer Feedback sentiment analysis
# 
# 
# To perform sentiment analysis on the provided JSON data, we can use Python libraries such as TextBlob or VADER from the nltk library. Below, I'll demonstrate how to use TextBlob to analyze the sentiment of each review.
# 
# 
# Explanation:
# Positive: The review expresses a positive sentiment.
# 
# Negative: The review expresses a negative sentiment.
# 
# Neutral: The review is neutral or mixed.
# 
# This script uses TextBlob to determine the sentiment of each review based on the polarity of the text. You can further customize or enhance the analysis by using more advanced NLP techniques or libraries like VADER or spaCy.

# ## Step 1 Install Required Libraries
# 

# First, ensure you have the necessary libraries installed. You can install them using pip:

# In[2]:


pip install textblob


# ## Step 2: Perform Sentiment Analysis

# Here's a Python script that reads the JSON data, performs sentiment analysis on each review, and outputs the results:

# In[7]:


from textblob import TextBlob
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

reviews_df = pd.read_json(r"C:\Users\jki\Desktop\NLP Projects\Kaptagat Springs Custyomer Feedback LLM\data\feedback.json")

reviews_df.head(5)


# In[10]:


# Function to perform sentiment analysis
def analyze_sentiment(review):
    analysis = TextBlob(review)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Analyze each review
for index, row in reviews_df.iterrows():
    product = row["product"]
    review = row["review"]
    sentiment = analyze_sentiment(review)
    print(f"Product: {product}, Review: {review}, Sentiment: {sentiment}")


# In[11]:


import json

# Function to perform sentiment analysis
def analyze_sentiment(review):
    analysis = TextBlob(review)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
reviews_df["sentiment"] = reviews_df["review"].apply(analyze_sentiment)

# Convert DataFrame to JSON format
sentiment_json = reviews_df.to_json(orient="records", indent=4)

# Save to a JSON file
output_path = "sentiment_results.json"
with open(output_path, "w") as json_file:
    json_file.write(sentiment_json)

print(f"Sentiment data saved successfully to {output_path}")


# In[ ]:





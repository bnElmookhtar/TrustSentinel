from flask import Flask, request, jsonify, render_template, redirect, url_for
import pickle
import os

app = Flask(__name__)  # Set frontend as template folder

# Load model & vectorizer
model = pickle.load(open("models/SPAM/models/spam_model.pkl", "rb"))
vectorizer = pickle.load(open("models/SPAM/models/tfidf_vectorizer.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")  # Home page


@app.route('/sms')
def sms_detector():
    return render_template("sms.html")  # SMS prediction page

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the data from the request
    sms_text = data['message']  # Use 'message' here, not 'text'

    # Preprocess the SMS text (Vectorize, Predict, etc.)
    sms_vectorized = vectorizer.transform([sms_text])  # Transform the text into a feature vector using the vectorizer

    # Make a prediction using the loaded model
    prediction = model.predict(sms_vectorized)

    # Return the result as JSON ( Spam or  Not Spam)
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)

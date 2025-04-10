from flask import Flask, request, jsonify, render_template
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load SMS model and vectorizer
smsModel = pickle.load(open("models/SPAM/models/spam_model.pkl", "rb"))
smsVectorizer = pickle.load(open("models/SPAM/models/tfidf_vectorizer.pkl", "rb"))

# Load Email model and tokenizer
emailModel = load_model("models/PHYSHING/models/lstm.h5")
with open("models/PHYSHING/models/lstm_tokenizer.pkl", "rb") as f:
    emailTokenizer = pickle.load(f)

MAX_SEQUENCE_LENGTH = 200  # لازم نفس الطول اللي استخدمته أثناء التدريب

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/email')
def email_page():
    return render_template("email.html")

@app.route('/predict_email', methods=['POST'])
def predict_email():
    data = request.get_json()
    email_text = data['message']
    
    sequence = emailTokenizer.texts_to_sequences([email_text])
    padded = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

    prediction = emailModel.predict(padded)
    predicted_label = "spam" if prediction[0][0] > 0.5 else "ham"

    return jsonify({'prediction': predicted_label})

@app.route('/sms')
def sms_page():
    return render_template("sms.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    sms_text = data['message']

    sms_vectorized = smsVectorizer.transform([sms_text])
    prediction = smsModel.predict(sms_vectorized)

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)

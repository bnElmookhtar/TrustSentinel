from flask import Flask, request, jsonify, render_template
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import smtplib
from email.mime.text import MIMEText
import joblib

app = Flask(__name__)

#Load Pages

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# صفحة من نحن
@app.route('/about')
def about():
    return render_template('About.html')

# صفحة تواصل معنا
@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/sentiment')
def sentiment():
    return render_template('sentiment.html')

@app.route('/email')
def email_page():
    return render_template("email.html")

@app.route('/sms')
def sms_page():
    return render_template("sms.html")

###########################Sending Email###########################
@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    full_message = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    msg = MIMEText(full_message)
    msg['Subject'] = 'New Contact Form Submission'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        with smtplib.starttls('smtp.gmail.com', 587) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return "<h3 style='color: green; text-align: center;'>Message sent successfully!</h3>"
    except Exception as e:
        return f"<h3 style='color: red; text-align: center;'>Failed to send email: {e}</h3>"

base_dir = os.path.dirname(os.path.abspath(__file__))
################# Models ####################
# Load SMS model and vectorizer
vectorizer_path = os.path.join(base_dir, "models", "SPAM", "models", "tfidf_vectorizer.pkl")
sms_path = os.path.join(base_dir, "models", "SPAM", "models", "spam_model.pkl")

with open(sms_path, "rb") as s:
    smsmodel = pickle.load(s)
with open(vectorizer_path, "rb") as sv:
    smsVectorizer = pickle.load(sv)


# Load Email model and tokenizer
email_path = os.path.join(base_dir, "models", "PHYSHING", "models", "lstm.h5")

emailtokenizer_path = os.path.join(base_dir, "models", "PHYSHING", "models", "lstm_tokenizer.pkl")
#emailModel = load_model(email_path)
with open(emailtokenizer_path, "rb") as et:
    emailTokenizer = pickle.load(et)
  
    
# Load Sentiment model and vectorizer
 
sentvectorizer_path = os.path.join(base_dir, "models", "sentiment", "models", "sentiment_vectorizer.pkl")
sentimentmodel_path = os.path.join(base_dir, "models", "sentiment", "models", "sentiment_model.pkl")

sentimentVectorizer = joblib.load(sentvectorizer_path)    
sentimentmodel = joblib.load(sentimentmodel_path)


with open(sentimentmodel_path, "rb") as s:
    sentimentmodel = pickle.load(s)
with open(sentvectorizer_path, "rb") as sv:
    sentimentVectorizer = pickle.load(sv)





MAX_SEQUENCE_LENGTH = 200  # لازم نفس الطول اللي استخدمته أثناء التدريب

######################### Routes #########################
@app.route('/predict_sentiment', methods=['POST'])
def predict_sentiment():
    data = request.get_json()
    sent_text = data['message']

    sentiment_vectorized = sentimentVectorizer.transform([sent_text])
    prediction = sentimentmodel.predict(sentiment_vectorized)
    
    return render_template('result.html', prediction=prediction)

    #data = request.get_json()
    #sent_text = data['message']

    #sentiment_vectorized = sentimentVectorizer.transform([sent_text])
    #prediction = sentimentmodel.predict(sentiment_vectorized)

    #return jsonify({'prediction': prediction[0]})


@app.route('/predict_email', methods=['POST'])
def predict_email():
    data = request.get_json()
    email_text = data['message']
    
    sequence = emailTokenizer.texts_to_sequences([email_text])
    padded = pad_sequences(sequence, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

 #   prediction = emailModel.predict(padded)
    predicted_label = "spam" #if prediction[0][0] > 0.5 else "ham"

    return jsonify({'prediction': predicted_label})


@app.route('/predict_sms', methods=['POST'])
def predict_sms():
    data = request.get_json()
    sms_text = data['message']

    sms_vectorized = smsVectorizer.transform([sms_text])
    prediction = smsmodel.predict(sms_vectorized)

    return jsonify({'prediction': prediction[0]})


if __name__ == '__main__':
    app.run(debug=True)

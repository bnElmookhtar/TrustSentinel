from flask import Flask, request, jsonify, render_template
import pickle
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing import image
import numpy as np
import smtplib
from email.mime.text import MIMEText
import joblib
import librosa

# بيانات بريدك الإلكتروني
EMAIL_ADDRESS = 'emanelmaasarawi@gmail.com'      # ✨ غيّريه لبريدك
EMAIL_PASSWORD = 'erjq fitd frdw fbsb'   # ✨ استخدمي app password لو حساب Gmail


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

@app.route('/robocalls')
def robocalls_page():
    return render_template("robocalls.html")

@app.route('/URLDetector')
def URLDetector_page():
    return render_template("URLDetector.html")

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
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
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
email_path = os.path.join(base_dir, "models", "PHYSHING", "models", "logistic_regression_20250409_151938.pkl")
emailvectorizer_path = os.path.join(base_dir, "models", "PHYSHING", "models", "logistic_regression_vectorizer_20250409_151938.pkl")

emailVectorizer = joblib.load(emailvectorizer_path)    
emailmodel = joblib.load(email_path)



    
# Load Sentiment model and vectorizer
 
sentvectorizer_path = os.path.join(base_dir, "models", "sentiment", "models", "sentiment_vectorizer.pkl")
sentimentmodel_path = os.path.join(base_dir, "models", "sentiment", "models", "sentiment_model.pkl")

with open(sentimentmodel_path, "rb") as model_file:
    sentimentmodel = pickle.load(model_file)

# Load the TF-IDF vectorizer
with open(sentvectorizer_path, "rb") as vectorizer_file:
    sentimentVectorizer = pickle.load(vectorizer_file)
    
    
# Load URLDetector model and tokenizer
URLDetector_path = os.path.join(base_dir, "models", "URLDetector", "models", "qr_spoofing_detector.h5")
URLDetectormodel = load_model(URLDetector_path)


# Load Audio model and tokenizer
audio_path = os.path.join(base_dir, "models", "ROBOCALLS", "models", "robocall_classifier.h5")
audiomodel = load_model(audio_path)

MAX_SEQUENCE_LENGTH = 200  # لازم نفس الطول اللي استخدمته أثناء التدريب

######################### Routes #########################
@app.route('/predict_sentiment', methods=['POST'])
def predict_sentiment():
    data = request.get_json()
    sent_text = data['message']

    sentiment_vectorized = sentimentVectorizer.transform([sent_text])
    prediction = sentimentmodel.predict(sentiment_vectorized)
    label = "Positive" if prediction == 1 else "Negative"
    return jsonify({'prediction': prediction, 'label': label})


@app.route('/predict_email', methods=['POST'])
def predict_email():
    try:
        data = request.get_json(force=True)
        email_text = data.get('message', '')

        if not email_text:
            return jsonify({'error': 'No message provided'}), 400

        # استخدم transform مش texts_to_sequences
        email_vectorized = emailVectorizer.transform([email_text])

        prediction = emailmodel.predict(email_vectorized)
        
        # لو الموديل بيرجع احتمالية (احتمال spam)
        predicted_label = "spam" if prediction[0] > 0.5 else "ham"
        # أو لو بيرجع كلاس 0 أو 1
        # predicted_label = "spam" if prediction[0] == 1 else "ham"

        return jsonify({'prediction': predicted_label})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/predict_sms', methods=['POST'])
def predict_sms():
    data = request.get_json()
    sms_text = data['message']

    sms_vectorized = smsVectorizer.transform([sms_text])
    prediction = smsmodel.predict(sms_vectorized)

    return jsonify({'prediction': prediction[0]})


################## URL Detector
UPLOAD_QRimage_FOLDER = 'static/uploads/QRimage'
os.makedirs(UPLOAD_QRimage_FOLDER, exist_ok=True)  # ✅ ده بيضمن إن المجلد موجود حتى لو ماكنش موجود قبل كده
app.config['UPLOAD_QRimage_FOLDER'] = UPLOAD_QRimage_FOLDER

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(256, 256))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = URLDetectormodel.predict(img_array)[0][0]
    return "Spoofing" if prediction > 0.5 else "Legit"
@app.route('/predict_URL', methods=['POST'])
def predict_URL():
    result = None
    file_url = None
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_QRimage_FOLDER'], filename)
        file.save(filepath)

        # التنبؤ باستخدام النموذج
        result = predict_image(filepath)
        file_url = filepath

    # إعادة عرض النتيجة على نفس صفحة index
    return render_template('URLDetector.html', result=result, file_url=file_url)

 
 ################## audio Detector
UPLOAD_audio_FOLDER = 'static/uploads/audio'
os.makedirs(UPLOAD_audio_FOLDER, exist_ok=True)
app.config['UPLOAD_audio_FOLDER'] = UPLOAD_audio_FOLDER

def predict_audio_file(audio_path):
    # تحميل الصوت
    y, sr = librosa.load(audio_path, sr=22050)
    
    # استخراج MFCCs أو Mel spectrogram بالحجم الصح
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=128)  # خليه 128
    mfccs = mfccs[:, :157]  # تأكد إن العرض 157 (قصه لو أكتر)

    # لو أقل من 157، كمله بـ zeros
    if mfccs.shape[1] < 157:
        pad_width = 157 - mfccs.shape[1]
        mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')

    # دلوقتي mfccs شكله (128, 157)
    
    # تطبيع الشكل (normalization لو عايز حسب التدريب)
    mfccs = (mfccs - np.min(mfccs)) / (np.max(mfccs) - np.min(mfccs))  # اختياري لو دربت بكده

    # اضف axis جديد علشان يبقى (128, 157, 1)
    mfccs = np.expand_dims(mfccs, axis=-1)

    # واضف axis لل batch (1, 128, 157, 1)
    mfccs = np.expand_dims(mfccs, axis=0)

    # توقع
    prediction = audiomodel.predict(mfccs)
    predicted_class = np.argmax(prediction, axis=1)[0]

    # ترجمة الرقم إلى اسم
    labels = {0: 'Robocall', 1: 'Legitimate Call'}
    label_name = labels[predicted_class]

    return label_name

# راوت التوقع من ملف صوت
@app.route('/predict_audio', methods=['POST'])
def predict_audio_route():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        file_path = os.path.join(app.config['UPLOAD_audio_FOLDER'], file.filename)
        file.save(file_path)

        result = predict_audio_file(file_path)
        file_url = file_path  # علشان تستخدمه للعرض مثلاً

        return render_template('robocalls.html', result=result, file_url=file_url)
 
 
 




if __name__ == '__main__':
    app.run(debug=True)

# TrustSentinel

📂 spam-detection-ml
│── 📂 data
│   ├── spam-dataset.csv  # Raw dataset
│   ├── preprocessed.csv  # Cleaned dataset
│
│── 📂 notebooks
│   ├── 1-data-exploration.ipynb  # Exploratory Data Analysis (EDA)
│   ├── 2-preprocessing.ipynb  # Text cleaning, tokenization
│   ├── 3-model-training.ipynb  # Model selection & training
│   ├── 4-evaluation.ipynb  # Model performance evaluation
│
│── 📂 models
│   ├── spam_classifier.h5  # Trained deep learning model
│   ├── vectorizer.pkl  # TF-IDF or CountVectorizer
│
│── 📂 src
│   ├── preprocess.py  # Text cleaning functions
│   ├── train_model.py  # Model training script
│   ├── predict.py  # Load model and make predictions
│
│── 📂 api
│   ├── app.py  # Flask API for real-time spam detection
│
│── 📂 web
│   ├── index.html  # Frontend UI for testing the model
│   ├── style.css  # CSS for styling
│   ├── script.js  # JS for user interactions
│
│── 📂 tests
│   ├── test_model.py  # Unit tests for model accuracy
│
│── requirements.txt  # List of dependencies
│── README.md  # Documentation
│── .gitignore  # Ignore unnecessary files

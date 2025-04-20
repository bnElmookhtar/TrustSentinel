import nltk
import re
import numpy as np
from nltk.corpus import stopwords

def clean_msg(msg):
    nltk.download('stopwords')
    msg = msg.lower()
    msg = re.sub('[^a-zA-Z ]', '', msg)
    msg = msg.split()
    words_of_msg = [word for word in msg if word not in set(stopwords.words('english'))]
    preprocessed_msag = ' '.join(words_of_msg)
    return preprocessed_msag

def load_glove(file_path):
    word_vectors = {}
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.array(values[1:],dtype='float32')
            word_vectors[word] = vector
    return word_vectors


def text_to_vector(text,glove_vector_path):
    words = clean_msg(text)
    glove_vectors = load_glove(glove_vector_path)
    word_vectors_list = [glove_vectors[word] for word in words if word in glove_vectors]
    return np.mean(word_vectors_list, axis=0) if word_vectors_list else np.zeros(50)


from sklearn.metrics import accuracy_score, confusion_matrix
def train_model(model , x_train ,y_train,x_test,y_test):
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    return accuracy_score(y_test, y_predict) , confusion_matrix(y_test, y_predict)  



from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.ensemble import RandomForestClassifier
def classical_models():
    return  {
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier(),
    'Naive Bayes': GaussianNB(),
    'Multinomial Naive Bayes': MultinomialNB(),
    'Random Forest': RandomForestClassifier()
    }


import joblib
def save_model(model, model_name):
    joblib.dump(model, f'../models/{model_name}.pkl')
    
def save_vectorizer(vectorizer, vectorizer_name):
    joblib.dump(vectorizer, f'../models/{vectorizer_name}.pkl')  


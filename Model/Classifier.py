import string
import nltk
import re
import joblib
import pandas as pd

# Sample message from testing set
message = 'You have WON a guaranteed £1000 cash or a £2000 prize.' \
          'To claim yr prize call our customer service representative on'


def count_punct(text):
    count = sum([1 for char in text if char in string.punctuation])
    return round(count / (len(text) - text.count(" ")), 3) * 100


def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text


def classify(text_message, vectorizer, model):

    # Engineer Features
    text_length = len(message) - message.count(" ")
    percent_punctuation = count_punct(text_message)

    # Vectorize Text
    tfidf_vect_message = vectorizer.transform(pd.DataFrame(data={'message': [text_message]})['message'])

    # Combine engineered features with vectorized text
    message_features = pd.concat([pd.DataFrame([{'message_length': text_length, 'punct%': percent_punctuation}]),
                                  pd.DataFrame(tfidf_vect_message.toarray(),
                                  columns=vectorizer.get_feature_names_out())], axis=1)

    # Predict
    prediction = model.predict(message_features)[0]

    return prediction


# Stopwords
stopwords = nltk.corpus.stopwords.words('english')
# Porter Stemmer object
ps = nltk.PorterStemmer()

# Load Vectorizer
vect = joblib.load('tfidf_vect_fit.pkl')
# Load Random Forest Model
rf_model = joblib.load('rf_model.pkl')

# Classify message
print(message, 'is:', classify(message, vect, rf_model))

from flask import Flask, render_template, request
from Classify import *
import joblib

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result", methods=['POST', 'GET'])
def result():
    # Get message from HTML form
    message = request.form["message"]

    # Print classification (spam/ham) to console
    message_class = classify(message, vectorize, random_forest_model)
    print(message_class)

    return render_template("result.html", status=message_class)


if __name__ == "__main__":
    # Load Vectorizer
    vectorize = joblib.load('Model/tfidf_vect_fit.pkl')
    # Load random forest model
    random_forest_model = joblib.load('Model/rf_model.pkl')

    app.run(debug=True)


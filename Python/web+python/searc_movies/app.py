from flask import Flask, render_template, request, redirect, url_for, flash
import requests

API_KEY = "16f03e335da07d1b33950f2b167af03c"
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

app=Flask(__name__)
@app.route('/')
def home():
    response = requests.get(BASE_URL, params={"api_key": API_KEY, "language": "ro-RO"})
    data = response.json()
    print(data)
    return render_template("main.html")


if __name__=="__main__":
    app.run(debug=True)

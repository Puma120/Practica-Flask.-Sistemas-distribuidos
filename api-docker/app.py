from flask import Flask

app = Flask(__name__)

@app.get('/')
def home():
    return {"status": "ok", "msg": "Welcome to the Flask API from Docker! (´▽`ʃ♡ƪ)"}
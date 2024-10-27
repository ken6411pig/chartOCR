# keep_alive.py
from flask import Flask
from threading import Thread
import time
import requests

app = Flask('')

@app.route('/')
def home():
    return "Server is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
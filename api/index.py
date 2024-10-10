from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World Vercelllll!'

@app.route('/about')
def about():
    return 'About. is also vercel'
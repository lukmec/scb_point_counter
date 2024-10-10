# app.py
# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/', methods=['GET'])
# def home():
#     return "Homepage"
#
#
# @app.route('/contact', methods=['GET'])
# def contact():
#     return "Contact page"
#

# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():
#     return 'Hello from Koyeb'
#
# @app.route('/2')
# def hello_world2():
#     return 'Hello from Koyeb 22222222'
#
#
# if __name__ == "__main__":
#     app.run()

from api.index import app

if __name__ == "__main__":
    app.run()
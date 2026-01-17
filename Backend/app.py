from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guitar_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9238hff29ufh92f209j23-9'

api = Api(app)
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return jsonify({"message": "Работает аааа?"})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    JWTManager, get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_jwt
)
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guitar_base.db'
app.config['JWT_SECRET_KEY'] = '834g93gb9ug34u9njscd234kmpiq3jipwuo3v55vu94fpi53foqfm3ipw7vu959uw'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"message": "Токен отсутствует"}), 401

@jwt.token_in_blocklist_loader
def check(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = Token_Black_list.query.filter_by(jti=jti).first()
    return token is not None

class Token_Black_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    revoked_on = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Register(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Пользователь уже существует'}, 400
        
        new_user = User(
            first_name=data['first_name'],
            last_name=data.get('last_name', ''),
            email=data['email'],
            password=generate_password_hash(data['password'])
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'Регистрация успешна'}, 201
        except Exception as e:
            return {'message': 'Ошибка БД'}, 500

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            
            resp = make_response(jsonify({
                'message': 'Вход выполнен',
                'user_id': user.id,
                'first_name': user.first_name
            }), 200)
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        return {'message': 'Неверные данные'}, 401

class Logout(Resource):
    @jwt_required(refresh=True)
    def get(self):
        jti = get_jwt()['jti']
        db.session.add(Token_Black_list(jti=jti))
        db.session.commit()
        resp = make_response(jsonify({'message': 'Выход выполнен'}), 200)
        unset_jwt_cookies(resp)
        return resp

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Logout, '/api/logout')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from utils import read_json, write_json

USERS_FILE = 'db/users.json'
auth_bp = Blueprint('auth', __name__)
api = Namespace('auth', description='Authentication related operations')

# ✅ Define Swagger models
user_model = api.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/register')
class Register(Resource):
    @api.expect(user_model)
    def post(self):
        users = read_json(USERS_FILE)
        data = request.get_json()
        if any(u['username'] == data['username'] for u in users):
            return {'msg': 'User already exists'}, 409

        user = {
            "id": len(users) + 1,
            "username": data['username'],
            "password": generate_password_hash(data['password'])
        }
        users.append(user)
        write_json(USERS_FILE, users)
        return {'msg': 'User registered successfully'}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(user_model)
    def post(self):
        users = read_json(USERS_FILE)
        data = request.get_json()
        user = next((u for u in users if u['username'] == data['username']), None)
        if user and check_password_hash(user['password'], data['password']):
            token = create_access_token(identity=user['id'])
            return {'token': token}
        return {'msg': 'Invalid credentials'}, 401

# src/services/user_service.py
from src.models.db import db
from src.models.user import User
from werkzeug.security import generate_password_hash

class UserService:

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def create_user(data):
        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        new_user.password_hash = generate_password_hash(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None

        user.username = data['username']
        user.email = data['email']
        if 'password' in data and data['password']:
            user.password_hash = generate_password_hash(data['password'])
        if 'role' in data:
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = data['is_active']

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return None

        db.session.delete(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return User.query.all()
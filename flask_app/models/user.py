from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
NAME_REGEX = re.compile(r'^[a-zA-z]')
PASSWORD_REGEX = re.compile(r'^(?=.*[0-9]$)(?=.*[a-zA-Z])')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('users_and_paintings_schema').query_db(query, data)

    @classmethod
    def get_user_info(cls, email):
        data = { 'email' : email}
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('users_and_paintings_schema').query_db(query, data)
        if (len(results) < 1):
            return False
        else:
            user = cls(results[0])
            return user

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if not (NAME_REGEX.match(user['first_name']) and len(user['first_name']) > 1):
            flash("First name is not valid.", 'registration')
            is_valid = False
        if not (NAME_REGEX.match(user['last_name']) and len(user['last_name']) > 1):
            flash("Last name is not valid.", 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']) or User.get_user_info(user['email']):
            flash("Email is either not valid or already has an account.", 'registration')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password is too short. Please make it at least 8 characters.", 'registration')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash("Password has to contain at least one letter and at least one number.", 'registration')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords did not match. Please make sure you put the same password in both fields.", 'registration')
            is_valid = False
        return is_valid

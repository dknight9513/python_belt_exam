from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
from flask_app.models.user import User

class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.user_id = data['user_id']
        self.quantity_purchased = data['quantity_purchased']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.painter = None
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, quantity, user_id, created_at, updated_at, quantity_purchased) VALUES ( %(title)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s, NOW(), NOW(), 0);"
        return connectToMySQL('users_and_paintings_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL('users_and_paintings_schema').query_db(query,data)

    @classmethod
    def buy_painting(cls,data):
        query = "UPDATE paintings SET quantity_purchased = %(quantity_purchased)s WHERE id = %(id)s;"
        connectToMySQL('users_and_paintings_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s"
        connectToMySQL('users_and_paintings_schema').query_db(query, data)

    @classmethod
    def new_owner(cls, data):
        query = "INSERT INTO purchased SET user_id = %(user_id)s, painting_id = %(id)s;"
        connectToMySQL('users_and_paintings_schema').query_db(query, data)

    @classmethod
    def get_all_paintings(cls):
        all_paintings = []
        query = "SELECT * FROM paintings"
        results = connectToMySQL('users_and_paintings_schema').query_db(query)
        for result in results:
            data = {
                'id' : result['id'],
                'title' : result['title'],
                'description' : result['description'],
                'price' : result['price'],
                'quantity' : result['quantity'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'user_id' : result['user_id']
            }
            all_paintings.append(cls(data))
        return all_paintings

    @classmethod
    def get_painting(cls, data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        result = connectToMySQL('users_and_paintings_schema').query_db(query, data)
        if len(result) == 0:
            return False
        result = result[0]
        painting_data = {
            'id' : result['id'],
            'title' : result['title'],
            'description' : result['description'],
            'price' : result['price'],
            'quantity' : result['quantity'],
            'quantity_purchased' : result['quantity_purchased'],
            'created_at' : result['created_at'],
            'updated_at' : result['updated_at'],
            'user_id' : result['user_id']
        }
        painting = cls(painting_data)
        return painting

    @classmethod
    def get_painting_and_user(cls, data):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(id)s;"
        result = connectToMySQL('users_and_paintings_schema').query_db(query, data)
        if len(result) == 0:
            return False
        result = result[0]
        painting_data = {
            'id' : result['id'],
            'title' : result['title'],
            'description' : result['description'],
            'price' : result['price'],
            'quantity' : result['quantity'],
            'quantity_purchased' : result['quantity_purchased'],
            'created_at' : result['created_at'],
            'updated_at' : result['updated_at'],
            'user_id' : result['user_id']
        }
        painting = cls(painting_data)
        user_data = {
            'id' : result['users.id'],
            'first_name' : result['first_name'],
            'last_name' : result['last_name'],
            'email' : result['email'],
            'password' : result['password'],
            'created_at' : result['users.created_at'],
            'updated_at' : result['users.updated_at']
        }
        user = User(user_data)
        painting.painter = user
        return painting

    @classmethod
    def get_all_paintings_and_users(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL('users_and_paintings_schema').query_db(query)
        all_paintings_users = []
        for result in results:
            painting_data = {
                'id' : result['id'],
                'title' : result['title'],
                'description' : result['description'],
                'price' : result['price'],
                'quantity' : result['quantity'],
                'quantity_purchased' : result['quantity_purchased'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'user_id' : result['user_id']
            }
            painting = cls(painting_data)
            user_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }
            user = User(user_data)
            painting.painter = user
            all_paintings_users.append(painting)
        return all_paintings_users

    @classmethod
    def get_all_purchased_paintings(cls, data):
        query = "SELECT * FROM paintings LEFT JOIN purchased ON purchased.painting_id = paintings.id LEFT JOIN users ON paintings.user_id = users.id WHERE purchased.user_id = %(id)s;"
        results = connectToMySQL('users_and_paintings_schema').query_db(query, data)
        all_paintings_users = []
        for result in results:
            painting_data = {
                'id' : result['id'],
                'title' : result['title'],
                'description' : result['description'],
                'price' : result['price'],
                'quantity' : result['quantity'],
                'quantity_purchased' : result['quantity_purchased'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at'],
                'user_id' : result['user_id']
            }
            painting = cls(painting_data)
            user_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }
            user = User(user_data)
            painting.painter = user
            all_paintings_users.append(painting)
        return all_paintings_users

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 2:
            flash("Painting title is too short. Must be at least 2 characters")
            is_valid = False
        if len(painting['description']) < 10:
            flash("Description is too short. Must be at least 10 characters")
            is_valid = False
        if not float(painting['price']) > 0:
            flash("Price must be greater than 0.")
            is_valid = False
        if not int(painting['quantity']) > 0:
            flash("Quantity must be greater than 0.")
            is_valid = False
        return is_valid

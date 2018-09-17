# coding: utf-8
from flask_login import UserMixin

class User(UserMixin):
    """
    user object
    """
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username , key='secret_key')


class UsersRepository:
    """
    manage users
    """
    def __init__(self):
        self.users = dict() #user.username : user
        self.users_id_dict = dict() #user.id : user
        self.identifier = 0

    def save_user(self , user):
        self.users.setdefault(user.username , user)
        self.users_id_dict.setdefault(user.id , user)

    def get_user(self , username):
        return self.users.get(username)

    def get_user_by_id(self , userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier +=1
        return self.identifier

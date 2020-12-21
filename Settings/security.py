from werkzeug.security import safe_str_cmp
from Model.user import User

users = [
    User(1, 'Saravanan', '@123'),
    # User(2, 'Kamakodu Raghuprasad', '@321'),
]

username_table = {u.username: u for u in users}

userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    userid = payload['identity']
    return userid_table.get(userid, None)

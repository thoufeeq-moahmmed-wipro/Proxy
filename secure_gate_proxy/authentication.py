USERS = {"admin": "admin123"}

def authenticate(username, password):
    return USERS.get(username) == password

# authentication.py

class Authentication:
    def __init__(self):
        self.valid_users = {
            "admin": "password123",
            "user1": "securepass",
            "user2": "mypassword"
        }

    def is_authenticated(self, username, password):
        """Check if the username and password are valid."""
        return self.valid_users.get(username) == password

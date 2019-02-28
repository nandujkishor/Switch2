from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, data, staff=None):
        self.id = id
        self.data = data
        self.staff = staff

    def super(self):
        return self.data.get('email')=="nandujkishor@gmail.com" or self.data.get('email')=="aswanth366@gmail.com" or self.data.get('email')=="bvsabhishek@gmail.com"

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, data, staff=None):
        self.id = id
        self.data = data
        self.staff = staff

    def super(self):
        return self.email=="nandujkishor@gmail.com" or self.email=="aswanth366@gmail.com"
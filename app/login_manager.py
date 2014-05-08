from bottle import request, response
from .models import User


class LoginManager(object):
    name = 'login_manager'
    api = 2

    def __init__(self, key='login_manager', secret=None):
        self.key = key
        self.secret = secret
        self.app = None

    def setup(self, app):
        self.app = app
        self.app.hooks.add('before_request', self.load_user)
        self.app.hooks.add('after_request', self.set_user)
        self.app.current_user = None
        self.app.login = self.login
        self.app.logout = self.logout

    def load_user(self):
        usermail = request.get_cookie(self.key, secret=self.secret)
        if usermail is not None:
            self.app.current_user = User.get(User.mail == usermail)

    def login(self, user):
        self.app.current_user = user
        self.set_user()

    def logout(self):
        self.app.current_user = None

    def set_user(self):
        if self.app.current_user is not None:
            response.set_cookie(name=self.key, 
                value=self.app.current_user.mail, secret=self.secret)
        response.delete_cookie(self.key)

    def apply(self, callback, context):
        return callback

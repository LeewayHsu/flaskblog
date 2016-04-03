#! flask/bin/python
class User(object):
    password_hash = '0'
    @property 
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = password+'111'

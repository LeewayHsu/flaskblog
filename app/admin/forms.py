#!flask/bin/python
# -*- coding: utf-8 -*-from flask.ext.wtf import Form

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class UserForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired()])
    nickname = StringField(u'昵称', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
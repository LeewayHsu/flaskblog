#!flask/bin/python
# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class PostForm(Form):
    title = StringField(u'标题', validators=[DataRequired()])
    body = StringField()
    markdown_resource = StringField()


class CommentForm(Form):
    nickname = StringField(u'昵称')
    email = StringField(u'邮箱')
    body = StringField(u'评论', validators=[DataRequired()])
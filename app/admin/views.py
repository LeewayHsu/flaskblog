#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from flask.ext.login import login_required,login_user,logout_user,current_user
from .import admin, forms
from ..models import User


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return render_template("admin.html")


@admin.route('/user/create', methods=['GET', 'POST'])
def create_user():
    form = forms.UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, nickname=form.nickname.data)
        user.password = form.password.data

        db.session.add(user)
        db.session.commit()
    return render_template("create_user.html",form=form)

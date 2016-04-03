#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, g, flash, request
from flask.ext.login import login_required,login_user,logout_user,current_user
from .import auth, forms
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('admin.index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(u'邮箱不存在！')
            return redirect(url_for('.login'))
        if (user.verify_password(form.password.data)):
            login_user(user, remember=form.remember_me.data)
        else:
            flash(u'密码不正确！')
            return redirect(url_for('.login', email=request.form.get("email")))
        return redirect(url_for('main.index'))
    if request.args.get("email") != "":
        form.email.data = request.args.get("email")
    return render_template("auth/login.html", form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
#!flask/bin/python
# -*- coding: utf-8 -*-
import datetime
from flask import render_template, url_for, redirect, g, flash, request

from .import main
from app.main import forms

from flask.ext.login import login_required, login_user, logout_user, current_user
from app import login_manager, db
from ..models import Post, Comment


@main.route('/')
@main.route('/index')
def index():
    posts = Post.query.filter_by(is_published=True).order_by('edit_time').paginate(1, 4, False).items
    return render_template("index.html", posts=posts)


@main.route('/post/list', methods=['GET'])
@main.route('/post/list/<int:page>', methods=['GET'])
@login_required
def post_list(page=1):
    pagination = Post.query.order_by('edit_time').paginate(page, 10, False)
    return render_template("post_list.html", pagination=pagination, route_='.post_list')


@main.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = forms.PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    markdown_resource=request.form["editormd-markdown-doc"],
                    body=request.form["editormd-html-code"],
                    user_id=int(current_user.id),
                    create_time=datetime.datetime.now(),
                    edit_time=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        flash(u"添加成功！")
        return redirect(url_for('.post_list'))
    return render_template("create_post.html", form=form)


@main.route('/post/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = forms.PostForm()
    post = Post.query.get(int(id))
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = request.form["editormd-html-code"]
        post.markdown_resource = request.form["editormd-markdown-doc"],
        post.edit_time = datetime.datetime.now()
        db.session.add(post)
        db.session.commit()
        flash(u"修改成功！")
        return redirect(url_for('.post_list'))
    form.title.data = post.title
    form.body.data = post.body
    form.markdown_resource.data = post.markdown_resource
    return render_template("create_post.html", form=form)


@main.route('/post/delete/<id>', methods=['GET'])
def delete_post(id):
    post = Post.query.get(int(id))
    db.session.delete(post)
    db.session.commit()
    flash(u"删除成功！")
    return redirect(url_for('.post_list'))


@main.route('/post/publish/<id>', methods=['GET'])
def publish_post(id):
    post = Post.query.get(int(id))
    post.is_published = True
    db.session.commit()
    flash(u"发布成功！")
    return redirect(url_for('.post_list'))


@main.route('/post/notpublish/<id>', methods=['GET'])
def not_publish_post(id):
    post = Post.query.get(int(id))
    post.is_published = False
    db.session.commit()
    flash(u"取消发布成功！")
    return redirect(url_for('.post_list'))


@main.route('/p/')
@main.route('/p/index')
@main.route('/p/?<int:page>', methods=['GET'])
@main.route('/p/index/?<int:page>', methods=['GET'])
def post_index(page=1):
    pagination = Post.query.filter_by(is_published=True).order_by('edit_time').paginate(page, 10, False)
    return render_template("post_index.html", pagination=pagination, route_='main.post_index')


@main.route('/p/<id>')
def post_details(id):
    post = Post.query.get(int(id))
    form = forms.CommentForm()

    return render_template("post.html", post=post, form=form)


@main.route('/comment/<post_id>', methods=['POST'])
def comment(post_id):
    form = forms.CommentForm()
    if form.validate_on_submit():
        comment = Comment(nickname=form.nickname.data,
                          email=form.email.data,
                          create_time=datetime.datetime.now(),
                          body=form.body.data,
                          post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash(u"评论成功！")
        return redirect(url_for('main.post_details',id=1))
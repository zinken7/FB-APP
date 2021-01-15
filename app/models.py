# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2020 -zinken7
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Float, JSON, Boolean, ForeignKey

from app import db, login_manager

from app.auth.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

class Customer(db.Model, UserMixin):

    __tablename__ = 'customers'

    id  = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    triggered = Column(Boolean, )

    def __init__(self, uid, triggered):
        self.uid = uid
        self.triggered = triggered

    def __repr__(self):
        return str(self.uid)

class Asset(db.Model, UserMixin):

    __tablename__ = 'assets'

    id  = Column(Integer, primary_key=True)
    a_key = Column(String, unique=True, nullable=False)
    a_val = Column(String, unique=True, nullable=True)

    def __init__(self, a_key, a_val):
        self.a_key = a_key
        self.a_val = a_val

    def __repr__(self):
        return str(self.id)

class Keyword(db.Model, UserMixin):

    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    l_dict = Column(JSON, )
    u_dict = Column(JSON, )

    def __init__(self, l_dict, u_dict):
        self.l_dict = l_dict
        self.u_dict = u_dict

    def __repr__(self):
        return str(self.id)

class Wordbook(db.Model, UserMixin):

    __tablename__ = 'wordbooks'

    id = Column(Integer, primary_key=True)
    w_val  = Column(String, )

    def __init__(self, w_val):
        self.w_val = w_val

    def __repr__(self):
        return str(self.id)

class ButtonData(db.Model, UserMixin):

    __tablename__ = 'buttons'

    id = Column(Integer, primary_key=True)
    name = Column(String, )
    u_name = Column(String, unique=True)
    val = Column(JSON, )

    def __init__(self, name, u_name, val):
        self.name = name
        self.u_name = u_name
        self.val = val

    def __repr__(self):
        return str(self.id)

class QuickReplies(db.Model, UserMixin):

    __tablename__ = 'quickreplies'

    id = Column(Integer, primary_key=True)
    name = Column(String, )
    u_name = Column(String, unique=True)
    val = Column(JSON, )

    def __init__(self, name, u_name, val):
        self.name = name
        self.u_name = u_name
        self.val = val

    def __repr__(self):
        return str(self.id)

class Welcome(db.Model, UserMixin):

    __tablename__ = 'welcomes'

    id = Column(Integer, primary_key=True)
    value  = Column(String, )

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.id)

class CommentData(db.Model, UserMixin):

    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    value  = Column(String, )

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.id)

class PersistentMenu(db.Model, UserMixin):

    __tablename__ = 'per_menus'

    id = Column(Integer, primary_key=True)
    stype  = Column(String, )
    title  = Column(String, )
    block  = Column(String, )

    def __init__(self, stype, title, block):
        self.stype = stype
        self.title = title
        self.block = block

    def __repr__(self):
        return str(self.id)

class FacebookUser(db.Model, UserMixin):

    __tablename__ = 'facebookusers'

    id  = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False, default=666666)
    u_token = Column(String, unique=True, nullable=True)
    app_id = Column(String, unique=True, nullable=True)
    app_secret = Column(String, unique=True, nullable=True)
    verify_token = Column(String, unique=True, nullable=True)
    p_id = Column(String, unique=True, nullable=True)
    p_token = Column(String, unique=True, nullable=True)

    def __init__(self, uid, u_token, app_id, app_secret, verify_token, p_id, p_token):
        self.uid = uid
        self.u_token = u_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.verify_token = verify_token
        self.p_id = p_id
        self.p_token = p_token

    def __repr__(self):
        return str(self.id)

class FacebookPage(db.Model, UserMixin):

    __tablename__ = 'facebookpages'

    id  = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=True)
    avatar = Column(String, nullable=True)
    name = Column(String, nullable=True)
    selected = Column(Boolean, default=False)

    def __init__(self, uid, avatar, name, selected):
        self.uid = uid
        self.avatar = avatar
        self.name = name
        self.selected = selected

    def __repr__(self):
        return str(self.id)

class Posts(db.Model):

    __tablename__ = 'posts_page'

    id = Column(Integer, primary_key=True)
    ppid = Column(String, unique=True, nullable=False)
    avatar = Column(String, nullable=True)
    name = Column(String, nullable=True)
    content = Column(String, nullable=True)
    comments = db.relationship('Comments', backref='post_id', lazy='dynamic')

    def __init__(self, ppid, avatar, name, content):
        self.ppid = ppid
        self.avatar = avatar
        self.name = name
        self.content = content

    def __repr__(self):
        return str(self.id)

class Comments(db.Model):

    __tablename__ = 'comments_post'

    id = Column(Integer, primary_key=True)
    pcid = Column(String, unique=True, nullable=True)
    uid = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    name = Column(String, nullable=True)
    content = Column(String, nullable=True)
    page_post_id = Column(String, ForeignKey('posts_page.ppid'), nullable=False)
    comments = db.relationship('Lv2Comments', backref='cmt_id', lazy='dynamic')

    def __init__(self, pcid, uid, avatar, name, content, page_post_id):
        self.pcid = pcid
        self.uid = uid
        self.avatar = avatar
        self.name = name
        self.content = content
        self.page_post_id = page_post_id

    def __repr__(self):
        return str(self.id)

class Lv2Comments(db.Model):

    __tablename__ = 'comments_comment'

    id = Column(Integer, primary_key=True)
    pcid = Column(String, unique=True, nullable=True)
    uid = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    name = Column(String, nullable=True)
    content = Column(String, nullable=True)
    comment_post_id = Column(String, ForeignKey('comments_post.pcid'), nullable=False)

    def __init__(self, pcid, uid, avatar, name, content, comment_post_id):
        self.pcid = pcid
        self.uid = uid
        self.avatar = avatar
        self.name = name
        self.content = content
        self.comment_post_id = comment_post_id

    def __repr__(self):
        return str(self.id)

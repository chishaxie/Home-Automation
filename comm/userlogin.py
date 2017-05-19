#!/usr/bin/env python
# -*- coding: utf8 -*-

import hashlib

import MySQLdb

'''
CREATE TABLE user
(
username varchar(64),
password varchar(32),
realname varchar(32),
PRIMARY KEY (username)
);
'''

def get_mysql_conn():
    return MySQLdb.connect(host='127.0.0.1',
        user='root', passwd='123456', db='ha', charset='utf8')

def fmt_password(password):
    pwd = hashlib.md5()
    pwd.update('xsvr_ha_' + password)
    return pwd.hexdigest()

class oaUser(object):
    def __init__(self, username, password, realname):
        self.username = username
        self.password = password
        self.realname = realname
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username

oa_user_cache = {}

def get_oa_user(username, password=None):
    if username in oa_user_cache:
        user = oa_user_cache[username]
        if password != None and fmt_password(password) != user.password:
            return None
        return user
    conn = get_mysql_conn()
    cur = conn.cursor()
    r = cur.execute("SELECT username, password, realname FROM user WHERE username = %s LIMIT 1", (username, ))
    conn.commit()
    if r != 1:
        return None
    rs = cur.fetchone()
    if password != None and fmt_password(password) != rs[1]:
        return None
    user = oaUser(rs[0], rs[1], rs[2])
    oa_user_cache[username] = user
    return user

def new_oa_user(username, password, realname):
    conn = get_mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO user (username, password, realname) VALUES (%s, %s, %s)", (username, fmt_password(password), realname))
    except Exception, e:
        return False, e
    conn.commit()
    return True, None

def set_oa_user(username, password):
    conn = get_mysql_conn()
    cur = conn.cursor()
    cur.execute("UPDATE user SET password = %s WHERE username = %s LIMIT 1", (fmt_password(password), username))
    conn.commit()
    if username in oa_user_cache:
        del oa_user_cache[username]
    return True

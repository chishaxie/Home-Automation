#!/usr/bin/env python
# -*- coding: utf8 -*-

import urllib

import logging

from flask import Blueprint, request, Response, render_template, redirect
from flask_login import login_required, login_user, logout_user, current_user

from comm import userlogin

api = Blueprint('ha', __name__, template_folder='templates')

logger = logging.getLogger('httpd.svr')

@api.route("/ha", methods=["GET"])
@login_required
def api_index():
    return render_template('index.html', username=current_user.get_id())

@api.route("/ha/login", methods=["GET"])
def api_login():
    return render_template('login.html')

@api.route("/ha/s/login", methods=["POST"])
def api_s_login():
    username = request.form.get('username')
    password = request.form.get('password')
    url = request.form.get('url')
    if not isinstance(password, basestring):
        password = ''
    user = userlogin.get_oa_user(username, password)
    if not user:
        return Response(u'账号和密码不匹配', mimetype='text/plain;charset=utf-8')
    logger.debug('ha login: %s', username)
    login_user(user)
    if url:
        url = urllib.unquote(url)
        return redirect(url)
    return redirect('/ha')

@api.route("/ha/logout", methods=["GET"])
@login_required
def api_logout():
    uname = current_user.get_id()
    logger.debug('ha logout: %s', uname)
    logout_user()
    return redirect('/ha')

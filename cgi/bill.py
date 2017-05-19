#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re
import json
import time
import thread
import random

import logging

import MySQLdb

from flask import Blueprint, request, Response, render_template, redirect
from flask_login import login_required, login_user, logout_user, current_user

api = Blueprint('bill', __name__)

logger = logging.getLogger('httpd.svr')

'''
CREATE TABLE bill
(
username       varchar(64),
timestamp      int,
timestamp2     int,
type           int,
money          int,
action         varchar(256),
effectiveness  int,
PRIMARY KEY (username, timestamp)
);
'''

def get_mysql_conn():
    return MySQLdb.connect(host='127.0.0.1',
        user='root', passwd='123456', db='ha', charset='utf8')

@api.route("/ha/bill", methods=["GET"])
@login_required
def api_bill():
    return render_template('bill.html', username=current_user.get_id())

@api.route("/ha/bill/s/show", methods=["POST"])
@login_required
def api_bill_s_show():
    conn = get_mysql_conn()
    cur = conn.cursor()
    r = cur.execute("SELECT username, timestamp, timestamp2, type, money, action, effectiveness FROM bill ORDER BY timestamp DESC")
    conn.commit()
    ds = cur.fetchmany(r)
    return Response(json.dumps({'ret': 0, 'ds': ds}), mimetype='text/json')

@api.route("/ha/bill/s/commit", methods=["POST"])
@login_required
def api_bill_s_commit():
    req = json.loads(request.get_data().decode('utf8'))
    logger.debug('%s commit %s', current_user.get_id(), req)
    conn = get_mysql_conn()
    cur = conn.cursor()
    cur_time = int(time.time())
    cur.execute("INSERT INTO bill (username, timestamp, type, money, action, effectiveness) VALUES (%s, %s, %s, %s, %s, %s)",
        (current_user.get_id(), cur_time, req["type"], req["money"], req["action"], 1))
    conn.commit()
    return Response(json.dumps({'ret': 0}), mimetype='text/json')

@api.route("/ha/bill/s/modify", methods=["POST"])
@login_required
def api_bill_s_modify():
    req = json.loads(request.get_data().decode('utf8'))
    logger.debug('%s modify %s', current_user.get_id(), req)
    conn = get_mysql_conn()
    cur = conn.cursor()
    cur.execute("UPDATE bill SET effectiveness = %s WHERE username = %s AND timestamp = %s",
        (req["effectiveness"], req["username"], req["timestamp"]))
    conn.commit()
    return Response(json.dumps({'ret': 0}), mimetype='text/json')

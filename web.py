#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys

import traceback
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask, render_template
from flask_login import LoginManager

logger = logging.getLogger('httpd.svr')

def init_log(log_obj, log_file, log_level=logging.DEBUG):
    formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)d <%(thread)d> %(levelname)-8s %(message)s')
    Rthandler = RotatingFileHandler(filename=log_file,
        maxBytes=10*1024*1024, backupCount=10)
    Rthandler.setFormatter(formatter)
    log_obj.addHandler(Rthandler)
    log_obj.setLevel(log_level)

init_log(logger, './log/httpd.log')

from comm import userlogin

from cgi.ha import api as api_ha
from cgi.bill import api as api_bill

app = Flask(__name__)

app.secret_key = 'eRq50sffS9px9WJd'
app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "/ha/login"

@login_manager.user_loader
def _user_loader(userid):
    return userlogin.get_oa_user(userid)

app.register_blueprint(api_ha)
app.register_blueprint(api_bill)

def contact_tb(tb):
    tb = traceback.extract_tb(tb)
    str_tb = 'Traceback (most recent call last):\n'
    for one in tb:
        tmp = '  '
        if len(one) == 4:
            tmp += '%s:%s %s(), %s' % (one[0], one[1], one[2], one[3])
        else:
            for x in one:
                tmp += str(x) + ' '
        str_tb += (tmp + '\n')
    return str_tb

@app.errorhandler(500)
def internal_error(error):
    exc_type, exc_info, tb = sys.exc_info()
    logger.error(exc_type)
    logger.error(error)
    str_tb = contact_tb(tb)
    logger.error(str_tb)
    return render_template('500.html'), 500

@app.errorhandler(400)
def bad_request(error):
    exc_type, exc_info, tb = sys.exc_info()
    logger.error(exc_type)
    logger.error(error)
    str_tb = contact_tb(tb)
    logger.error(str_tb)
    return render_template('404.html'), 400

@app.errorhandler(404)
def not_found(error):
    logger.warn(error)
    return render_template('404.html'), 404

if __name__ == '__main__':

    fhlog = logging.FileHandler('flask.log')
    fhlog.setLevel(logging.DEBUG)
    fllog = logging.getLogger('werkzeug')
    fllog.setLevel(logging.DEBUG)
    fllog.addHandler(fhlog)
    fllog.info('httpd is running ...')
    logger.info('httpd is running ...')
    print 'httpd is running ...'

    port = 8888
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        port = 19888

    app.run(host='0.0.0.0', port=port, debug=False,
        use_reloader=True, threaded=True)

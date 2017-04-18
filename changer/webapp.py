# coding: utf-8
'''web application with only one route'''
import logging

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from changer.FileChanger import FileChanger

APP = Flask(__name__, static_url_path='/static')

CHANGER = FileChanger(config_path='config.json')


@APP.route('/', methods=['GET', 'POST'])
def index():
    '''main route which render index page and process switching by POST'''
    title = CHANGER.config.get('main_title', u'Добро пожаловать!')
    if request.method == 'GET':
        return render_template('index.html',
                               maintitle=title, hosts=CHANGER.hosts)
    else:
        new_server = request.form.get('options')
        if new_server:
            logging.debug('POST %s', new_server)
            CHANGER.search_and_replace(new_server)
        return redirect(url_for('index'))

# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template
from changer.FileChanger import FileChanger
app = Flask(__name__, static_url_path='/static')

changer = FileChanger(config_path='config.json')

@app.route('/', methods=['GET', 'POST'])
def index():
    title = changer.config.get('main_title', u'Добро пожаловать!')
    if request.method == 'GET':
        return render_template('index.html', maintitle=title, hosts=changer.hosts)
    else:
        new_server = request.form.get('options')
        if new_server:
            print('POST', new_server)
            changer.search_and_replace(new_server)
        return redirect(url_for('index'))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    buttons = [
        {
            'key': 'mainserver',
            'text': 'Kodeks server',
            'checked': True,
        },
        {
            'key': 'reserveserver',
            'text': u'Резервный сервер',
            'checked': False,
        },
    ]
    return render_template('index.html', buttons=buttons)

if __name__ == '__main__':
    app.run()

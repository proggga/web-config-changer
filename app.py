#!/usr/bin/env python
from flask import Flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def hello_world():
    return 'Hello, World!'

from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
@app.route('/hello/<name>/')
def hello(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run()

#!/usr/bin/python
from flask import Flask, render_template
#from flask.ext.socketio import SocketIO, emit
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run('0.0.0.0')

import os
import json

import flask
from flask import request
app = flask.Flask(__name__)

button_presses = 0

@app.route('/', methods=['GET', 'POST'])
def front_page():
    global button_presses
    
    args = {}
    args["intro_text"] = "Generalizing Chomsky's famous sentence into syntactic singular vectors."
    args["title"]      = "flask-colorless"
    args["author"]     = "travis hoppe"
    args["author_url"] = "http://thoppe.github.io"
    args["button_status"] = "You have not pressed the button."

    if request.method == 'GET':
        button_presses = 0

    if request.method == 'POST':
        button_presses += 1
        msg = "The button has been pressed {} times"
        args["button_status"] = msg.format(button_presses)
    
    return flask.render_template('index.html', **args)

if __name__ == '__main__':
    app.debug = True
    app.run()

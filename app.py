import os
import json

import flask
from flask import request
app = flask.Flask(__name__)

import absurd_noun_pairs as ANP


@app.route('/', methods=['GET'])
def front_page():
    global button_presses
    
    args = {}
    args["title"]      = "Colorless green ideas"
    args["author"]     = "travis hoppe"
    args["author_url"] = "http://thoppe.github.io"
    args["project_url"] = "https://github.com/thoppe/Colorless-Green-Ideas"
    args["button_status"] = "You have not pressed the button."

    result_list = []

    for k in xrange(15):
        phrase, scores = ANP.quality_filter()
        result_list.append(' '.join(phrase))

    args["result_list"] = result_list
    return flask.render_template('index.html', **args)

if __name__ == '__main__':
    app.debug = True
    app.run()

import os
import json

import flask
from flask import request
app = flask.Flask(__name__)

import absurd_noun_pairs as ANP

_default_return_results = 15

def get_results(n):
    result_list = []
    for k in xrange(n):
        phrase, scores = ANP.quality_filter()
        result_list.append(' '.join(phrase))
    return result_list

@app.route('/API', defaults={"n" : _default_return_results})
@app.route('/API/<int:n>', methods=['GET'])
def text_results(n = _default_return_results):
    n = max(1,min(n,50))
    results = {"results":get_results(n)}
    return flask.jsonify(results)

@app.route('/', methods=['GET'])
def front_page():
    
    args = {}
    args["title"]       = "Colorless green ideas"
    args["author"]      = "travis hoppe"
    args["project_url"] = "https://github.com/thoppe/Colorless-Green-Ideas"
    args["result_list"] = get_results(_default_return_results)
    
    return flask.render_template('index.html', **args)

if __name__ == '__main__':
    app.debug = True
    app.run()

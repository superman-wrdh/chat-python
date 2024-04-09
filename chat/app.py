# -*- encoding: utf-8 -*-
from flask import Flask, request
from flask import render_template, jsonify
from chat.core import send_msg
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/", methods=["GET", "POST"])
def temp():
    return render_template('index.html')


@app.route("/chat", methods=["GET", "POST"])
def chat_user():
    input_json = request.get_json()

    msg = input_json['info']
    data = send_msg(msg)
    return jsonify(data)


if __name__ == '__main__':
    app.run()


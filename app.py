from recall.context import Context
from flask import Flask, jsonify, request
from recall.service import recall_service

app = Flask('recall-service')

@app.route("/")    ## recall 猜你喜欢
def get_anime():
    pass

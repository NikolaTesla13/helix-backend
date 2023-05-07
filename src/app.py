from src.rce import RemoteCodeExecution
from flask import Flask, request
import json

app = Flask(__name__)

@app.get("/")
def index():
    return "<p>Hello, World!</p>"

@app.post("/rce/run")
def run():
    body = request.get_json(silent=True)
    result = RemoteCodeExecution.execute_code(body["code"], body["input"])
    return result

@app.post("/rce/test")
def test():
    return "TODO"

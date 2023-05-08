from src.rce import RemoteCodeExecution
from flask import Flask, request

app = Flask(__name__)
rce_engine = RemoteCodeExecution()

@app.get("/")
def index():
    return "<p>Hello, World!</p>"

@app.post("/rce/run")
def run():
    body = request.get_json(silent=True)
    unsafe = request.args.get('unsafe')

    if unsafe == "true":
        result = rce_engine.unsafe_execute_code(body["code"], body["input"])
    else:
        result = rce_engine.execute_code(body["code"], body["input"])
        
    return result

@app.post("/rce/test")
def test():
    return "TODO"

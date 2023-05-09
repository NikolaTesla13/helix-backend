from src.rce import RemoteCodeExecution
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
rce_engine = RemoteCodeExecution()

app.config["CORS_HEADERS"] = "Content-Type"


@app.get("/")
def index():
    return "<p>Hello, World!</p>"


@app.post("/rce/run")
@cross_origin()
def run():
    body = request.get_json(silent=True)
    unsafe = request.args.get("unsafe")

    if unsafe == "true":
        result = rce_engine.unsafe_execute_code(body["code"], body["input"])
    else:
        result = rce_engine.execute_code(body["code"], body["input"])

    return result


@app.post("/rce/test")
@cross_origin()
def test_code():
    body = request.get_json(silent=True)
    result = rce_engine.unsafe_test_code(body["code"], body["tests"])
    return result


@app.post("/rce/test")
@cross_origin()
def test():
    return "TODO"

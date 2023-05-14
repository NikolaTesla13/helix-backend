from src.rce import RemoteCodeExecution
from src.ai import AIModelPredictor
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
rce_engine = RemoteCodeExecution()
ai_engine = AIModelPredictor()

app.config["CORS_HEADERS"] = "Content-Type"
app.config["CORS_ORIGINS"] = "https://helix-td2p.onrender.com"


@app.get("/")
def index():
    return "<p>Hello, World!</p>"


@app.post("/rce/run")
@cross_origin()
def run():
    body = request.get_json(silent=True)
    unsafe = request.args.get("unsafe")

    if unsafe == "true":
        result = rce_engine.unsafe_execute_code(
            body["lang"], body["code"], body["input"]
        )
    else:
        result = rce_engine.execute_code(body["code"], body["input"])

    return result


@app.post("/rce/test")
@cross_origin()
def test_code():
    body = request.get_json(silent=True)
    result = rce_engine.unsafe_test_code(body["lang"], body["code"], body["tests"])
    return result


@app.post("/ai/generate")
@cross_origin()
def generate_text():
    body = request.get_json(silent=True)
    result = ai_engine.generate(body["prompt"])
    return result


@app.post("/ai/summary")
@cross_origin()
def summary_text():
    body = request.get_json(silent=True)
    result = ai_engine.generate(body["prompt"])
    return result


@app.post("/ai/chat")
@cross_origin()
def chat():
    body = request.get_json(silent=True)
    result = ai_engine.chat(body["prompt"])
    return result


@app.post("/ai/code")
@cross_origin()
def code_completition():
    body = request.get_json(silent=True)
    result = ai_engine.code_completition(body["prompt"])
    return result

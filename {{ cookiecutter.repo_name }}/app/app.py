from flask import Flask, Response, request
import json
from logger.logger import get_logger
from config.config import LOGGER_CONFIG
from handlers.http import HTTPHandler
from handlers.predict import ModelPredict
from handlers import model

app = Flask(__name__)
logger = get_logger(LOGGER_CONFIG)
model = model.load(logger)


@app.route('/<SERVICE-PREFIX>/health', methods=['GET'])
def health():
    res = {"message": "I am alive"}
    return Response(json.dumps(res), 200, mimetype='application/json')


@app.route('/<SERVICE-PREFIX>/v1/predict', methods=['POST'])
def predict():
    req = HTTPHandler(request.get_json(), request.headers.get('X-Request-ID'))

    req_id, roi, err, res_stat = req.validate(logger)
    if err is not None:
        return Response(err, mimetype='application/json', status=res_stat.code)

    pred = ModelPredict(model, roi)
    res, err, res_stat = pred.run(req_id, logger)
    if err is not None:
        return Response(err, mimetype='application/json', status=res_stat.code)

    return Response(res, mimetype='application/json', status=res_stat.code)

from ctypes import ArgumentError
from flask import Flask, request
from catboost import CatBoostClassifier
import pandas as pd
import os.path
import json


class Model:
    fields = ['age', 'gender', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']

    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError
        self.model = CatBoostClassifier() 
        self.model.load_model(filename)

    def predict(self, data):
        for field in self.fields:
            if data.get(field, None) is None:
                raise ArgumentError
        fn_data = pd.DataFrame()
        for field in self.fields:
            fn_data[field] = [data[field]]
        pred = self.model.predict(fn_data)
        return pred[0]

model = None 

class Server:
    app = Flask(__name__)

    def __init__(self, host, port, model):
        self.host = host
        self.port = port
        self.model = model

    @app.route("/", methods=["POST"])
    def hello():
        if model is None:
            return "500"
        return json.dumps({"prediction": int(model.predict(request.get_json()))})
    
    def run(self):
        self.app.run(host=self.host, port=self.port)


if __name__ == "__main__":
    model = Model('server/catboost_iterations_135_depth_6')
    server = Server("0.0.0.0", 6969, model)
    server.run()

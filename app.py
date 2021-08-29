from flask import Flask, render_template, jsonify
import json
import numpy as np

import model

with open('data_struct.min.json') as jsondata:
    struct = json.load(jsondata)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/states')
def get_state(state_idx=None):
    if state_idx is None:
        return jsonify(struct["states"])
    return struct["states"][state_idx]

@app.route('/api/districts/<int:state_idx>')
def get_district(state_idx, district_idx=None):
    if district_idx is None:
        return jsonify(struct[get_state(state_idx)]["districts"])
    return struct[get_state(state_idx)]["districts"][district_idx]

@app.route('/api/markets/<int:state_idx>/<int:district_idx>')
def get_market(state_idx, district_idx, market_idx=None):
    if market_idx is None:
        return jsonify(struct[get_state(state_idx)][get_district(state_idx, district_idx)]["markets"])
    return struct[get_state(state_idx)][get_district(state_idx, district_idx)]["markets"][market_idx]

@app.route('/api/variety/<int:state_idx>/<int:district_idx>/<int:market_idx>')
def get_variety(state_idx, district_idx, market_idx, variety_idx=None):
    if variety_idx is None:
        return jsonify(struct[get_state(state_idx)][get_district(state_idx, district_idx)][get_market(state_idx, district_idx, market_idx)]["varieties"])
    return struct[get_state(state_idx)][get_district(state_idx, district_idx)][get_market(state_idx, district_idx, market_idx)]["varieties"][variety_idx]

@app.route('/api/history/<int:state>/<int:district>/<int:market>/<int:variety>/<int:mode>/<int:obs_no>')
def get_history(state, district, market, variety, mode, obs_no):
    np.random.seed(state+district+market+variety)
    prices = np.random.randint(3000, 4500, obs_no).tolist() # change this line
    return jsonify(prices)

@app.route('/api/predict/<int:state>/<int:district>/<int:market>/<int:variety>/<int:mode>/<int:obs_no>')
def week_prediction(state, district, market, variety, mode, obs_no):
    # prices = np.random.randint(10000, 35000, obs_no).tolist() # change this line
    prices = model.get_predict(market, variety, mode, obs_no)
    return jsonify(prices)

if __name__ == '__main__':
   app.run(debug = True)

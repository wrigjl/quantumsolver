'''This is the flask router for the quantum solver app'''

from flask import request
from app import app
import deutsch_classical
import bernstein_vazirani_classical

# pylint: disable=missing-function-docstring

@app.route('/')
@app.route('/index')
def index():
    return "Welcom to the quantum solver."

@app.route('/deutsch-classical', methods=['POST'])
def solver_deutsch_classical():
    if not request.is_json:
        return "expected json input"
    data = request.json
    return deutsch_classical.solve(data)

@app.route('/bernstein-vazirani-classical', methods=['POST'])
def solver_bz_classical():
    if not request.is_json:
        return "expected json input"
    data = request.json
    return bernstein_vazirani_classical.solve(data)

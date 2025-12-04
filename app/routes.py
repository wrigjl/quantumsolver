'''This is the flask router for the quantum solver app'''

from flask import request
from app import app
import deutsch_classical
import bernstein_vazirani_quantum
import deutsch_quantum
import deutsch_jozsa_quantum

# pylint: disable=missing-function-docstring

@app.route('/')
@app.route('/index')
def index():
    return "Welcome to the quantum solver."

@app.route('/deutsch-classical', methods=['POST'])
def solver_deutsch_classical():
    if not request.is_json:
        return "expected json input"
    data = request.json
    return deutsch_classical.solve(data)

@app.route('/deutsch-jozsa-quantum', methods=['POST'])
def solver_deutsch_jozsa_quantum():
    if not request.is_json:
        return "expected json input"
    data = request.json
    return deutsch_jozsa_quantum.solve(data)

@app.route('/bernstein-vazirani-quantum', methods=['POST'])
def solver_bz_quantum():
    if not request.is_json:
        return "expected json input"
    data = request.json
    return bernstein_vazirani_quantum.solve(data)

@app.route('/deutsch-quantum', methods=['POST'])
def solver_deutsch_quantum():
    if not request.is_json:
        return "expected json input"
    data = request.json
    return deutsch_quantum.solve(data)

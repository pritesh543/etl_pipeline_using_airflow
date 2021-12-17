"""This module provide a public endpoint to 
access resource in the system 
with basic authentication check"""

from flask import Blueprint, jsonify, request
api = Blueprint('api', __name__)

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# user module
from events import Events

users = {
            "john": "john@123",
            "peter" : "peter@123"
        }

@auth.verify_password
def authenticate(username, password):
    if not (username and password):
        return False
    return users.get(username) == password

def jsonifyEvents(**kwargs):
    return jsonify({
        **kwargs,
        "success" : True,
        "message" : "Events Retrieved Successfully !"
    })

@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@api.route('/api/events', methods=['GET'])
@auth.login_required
def get_events():
    input_args = {
        "event" : request.args.get('event',''),
        "from_timestamp" : request.args.get('from_timestamp',''),
        "to_timestamp" : request.args.get('to_timestamp','')
    }
    data = Events(**input_args).get_events()

    return jsonifyEvents(**data), 200

"""
REST API routes.

Defines endpoints for wines, producers, regions, and countries.
"""

from flask import request, jsonify
from app import app

#GET /wines
@app.route("/wines", methods=["GET"])
def get_wines():
    pass

#POST /wines
@app.route("/wines", methods=["POST"])
def add_wine():
    pass

#PUT /wines
@app.route("/wines", methods=["PUT"])
def update_wine():
    pass

#DELETE /wines
@app.route("/wines", methods=["DELETE"])
def remove_wine():
    pass

#GET /producers
@app.route("/producers", methods=["GET"])
def get_producers():
    pass

#GET /regions
@app.route("/regions", methods=["GET"])
def get_regions():
    pass

#GET /countries
@app.route("/countries", methods=["GET"])
def get_countries():
    pass

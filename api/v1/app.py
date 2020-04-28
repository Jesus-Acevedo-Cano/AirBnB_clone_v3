#!/usr/bin/python3
""" init flask files """


from os import getenv
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_(exc):
    """close session"""
    storage.close()


@app.errorhandler(404)
def error_404(msj):
    """Handler error 404"""
    msj = {"error": "Not found"}
    return(jsonify(msj), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

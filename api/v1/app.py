#!/usr/bin/python3
"""
Start API
app.py
"""

from flask import Flask
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

# register blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown function
    """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

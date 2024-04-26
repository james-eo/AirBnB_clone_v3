#!/usr/bin/python3
"""
views
"""

from flask import Blueprint

# wildcard import
from api.v1.views.index import *

app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

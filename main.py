from flask import Flask, request, render_template

from flask_caching import Cache

from typing import Dict, List

import re

config = {
    "DEBUG": True,           # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}



app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
@cache.cached(timeout=50)
def index():
    return render_template('index.html')

# read kamus
# Setup Index Page
# Use web form for user input
# process input, display result from Kamus

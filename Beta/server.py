from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests, json
from model import connect_to_db, db, Chirp

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRET!"
#raises an error for undefined variables
app.jinja_env.undefined = StrictUndefined

@app.route('/index')
def index():
    """Query database and return all chirps, ordered chronologically."""
    chirps = Chirp.query.order_by('c_id').all()
    return render_template("chirp_list.html", chirps=chirps)

@app.route('/create_chirp', METHODS=["POST"])
def create_chirp():
    return render_template("create_chirp.html")

if __name__ == "__main__":
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(debug=True, host="0.0.0.0", port=3000)


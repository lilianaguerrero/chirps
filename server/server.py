from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
import requests, json
from model import connect_to_db, db, Chirp
from sqlalchemy import desc

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRET!"
#raises an error for undefined variables
app.jinja_env.undefined = StrictUndefined

VOTED = []
@app.route('/index', methods=['GET','POST'])
def index():
    """Query database and return all chirps, ordered chronologically."""
    chirps = Chirp.query.order_by(desc('up_votes'),desc('c_id')).all()
    if request.method == "POST":
        up_voted_id = list(request.form.keys())[0]
        record_to_update = Chirp.query.get(up_voted_id)
        if request.form.get(up_voted_id) == 'Upvote':
            VOTED.append(int(up_voted_id))
            record_to_update.up_votes = record_to_update.up_votes + 1 
            print(VOTED)
        if request.form.get(up_voted_id) == 'Downvote':
            if record_to_update.up_votes > 0:
                record_to_update.up_votes = record_to_update.up_votes - 1 
        db.session.commit()
    return render_template("chirp_list.html", chirps=chirps, voted=VOTED)

@app.route('/create_chirp', methods=['GET','POST'])
def create_chirp():
    error = None

    if request.method == "POST":
        new_chirp = request.form.get('new_chirp')
        if len(new_chirp) < 1:
            error = "Error: enter atleast 1 character per Chirp"
        elif len(new_chirp) <= 140:
            #add & commit the new_chirp to db
            db_chirp = Chirp(text=new_chirp)
            db.session.add(db_chirp)
            db.session.commit()
            saved_chirp = db.session.query(Chirp).filter_by(text=new_chirp).first()
            push_notification(saved_chirp)
            return redirect(url_for('index'))
    return render_template("create_chirp.html", error=error)

@app.route("/push", methods=['POST'])
def push_notification(saved_chirp):
    url = 'https://bellbird.joinhandshake-internal.com/push'
    payload = {'chirp_id': saved_chirp.c_id}
    r = requests.post(url, params=payload)
    print(r.json)
    print(r.status_code) 
    # == slow_number:
    #     async process


if __name__ == "__main__":
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(debug=True, host="0.0.0.0", port=3000)


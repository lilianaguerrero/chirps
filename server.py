from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
import requests, json
from model import connect_to_db, db, Chirp
from sqlalchemy import desc

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "SECRET!"
#raises an error for undefined variables
app.jinja_env.undefined = StrictUndefined

SAVED_CHIRP = None
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
        #if request.form.get(p_voted_id) == 'Downvote':
            # decrement the up_vote in DB
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
            SAVED_CHIRP = db.session.query(Chirp).filter_by(text=new_chirp).first()
            #do post request to "/push  send SAVED_CHIRP"
            print("this is the saved chirp " + str(SAVED_CHIRP))
    return render_template("create_chirp.html", error=error)

@app.route("/push", methods=['POST'])
def push_notification(SAVED_CHIRP):
    # post request to push notification API pass though json data of 
    print("c_id" + str(SAVED_CHIRP))
    r = requests.post('http://example.com/index.php', params={'q': 'raspberry pi request'})
    return redirect(url_for('index'))
# will send push request to all users on local host 

if __name__ == "__main__":
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(debug=True, host="0.0.0.0", port=3000)


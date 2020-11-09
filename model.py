"""Models and database functions for Chirps project."""

#imports SQLAlchemy
from flask_sqlalchemy import SQLAlchemy 
#connection to the PostgreSQL database
db = SQLAlchemy()

#class = table
class Chirp(db.Model):
#Chirps table. Columns: id (PK), text (string 140 chars or less)

    __tablename__ = "chirps"

    c_id = db.Column(db.Integer,
                    autoincrement = True,
                    primary_key = True)
    text = db.Column(db.String(140),
                    nullable = False)
    def __repr__(self):
        """respresentation of the info"""
        return f"{self.c_id, self.text}"

# Helper function
def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///chirpdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def example_chirps():
    #Load example chirps into database
    print("Loading Chirps")
    chirps = ["this is the first chirp",
            "this is the second chirp "]
    for item in chirps:
        chirp = Chirp(text=item)
        # add to session so that it can be stored
        db.session.add(chirp)
    db.session.commit()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
    db.create_all()
    print("Coreated Table(s).")
    example_chirps()


    

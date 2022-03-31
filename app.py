from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art.db'

#initialise the database
db = SQLAlchemy(app)

#Create database model
class Art_pieces(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #Function to return a string of something
    def __repr__(self):
        return '<Name %r>' % self.id

subscribers = []

@app.route('/gallery', methods=["POST", "GET"])
def gallery():

    if request.method == "POST":
        piece_name = request.form["piece_name"]
        new_piece = Art_pieces(title=piece_name)

        #Push to db
        try:
            db.session.add(new_piece)
            db.session.commit()
            return redirect("/gallery")
        except:
            return "Error adding piece"

        return "You added something"
    else:
        pieces = Art_pieces.query.order_by(Art_pieces.date_created)
        return render_template("gallery.html", pieces=pieces)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    names =["Noah", "Charles", "Anastasia", "Dot", "Daamitha"]
    return render_template("about.html", names=names)

@app.route('/subscribe')
def subscribe():
    return render_template("subscribe.html")
    
#only allowed to come here if you have submitted a form to here
@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")

    if not first_name or not last_name or not email:
        error_statement = "All form fields required..."
        return render_template("subscribe.html", error_statement=error_statement, first_name=first_name, last_name=last_name, email=email)

    subscribers.append(f"{first_name} {last_name} | {email}")

    return render_template("form.html", subscribers=subscribers)

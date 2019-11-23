from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite'
db = SQLAlchemy(app)


class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxPlaces = db.Column(db.Integer)
    number = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    #nwm jak tutaj wiele uzytkownikow zrobic
    users = db.relationship("User", backref = "event")
    description = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DATE, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    auditorium = db.Column(db.Integer, db.ForeignKey('auditorium.id'))

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user')
def user_site():
    return render_template("user.html")


@app.route('/admin')
def admin_site():
    return render_template("admin.html")


if __name__ == '__main__':
    app.run()

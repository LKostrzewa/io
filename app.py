from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite'
db = SQLAlchemy(app)


class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxPlaces = db.Column(db.Integer)
    number = db.Column(db.Integer)

# klasa laczaca user z event ( bo jest to relacja many-to-many) - nazwe lepsza trzeba wybrac
tags = db.table('tags',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
                )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    # nwm jak tutaj wiele uzytkownikow zrobic
    # users = db.relationship("User", backref = "event")
    description = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DATE, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    auditorium = db.Column(db.Integer, db.ForeignKey('auditorium.id'))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('event', lazy=True))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user')
def user_site():
    return render_template("user.html")


@app.route('/admin')
def admin_site():
    return render_template("admin.html")

# to tylko wstepne ale nie ogarniam bazy totalnie czy to jest git w
# przypadku jak relacje bo to by była ta sama metoda dla kazdej tabeli xdd
@app.route('/admin/add-event')
def add_event(event):
    db.session.add(event)
    db.session.commit()


@app.route('/admin/delete-event')
def delete_event(event):
    db.session.delete(event)
    db.session.commit()


@app.route('/admin/get-event/<id>')
def get_event(id):
    return Event.query.get_or_404(id)


@app.route('/admin/all-events')
def get_all_event():
    return render_template('all-events.html',
                           events=Event.query.order_by(Event.id.desc()).all()
                           )


@app.route('/admin/get-auditorium/<id>')
def get_auditorium(id):
    return Auditorium.get(id)


if __name__ == '__main__':
    app.run()

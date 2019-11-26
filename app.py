from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite'
db = SQLAlchemy(app)


class Auditorium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxPlaces = db.Column(db.Integer)
    number = db.Column(db.Integer)


# klasa laczaca user z event ( bo jest to relacja many-to-many) - nazwe lepsza trzeba wybrac
tags = db.Table('tags',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
                )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # nwm jak tutaj wiele uzytkownikow zrobic
    # users = db.relationship("User", backref = "event")
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    # time = db.Column(db.Time)
    # auditorium = db.Column(db.Integer, db.ForeignKey('auditorium.id'))
    # tags = db.relationship('User', secondary=tags, lazy='subquery',
    #                        backref=db.backref('event', lazy=True))

    def __init__(self, id, name, description, date):#, auditorium, tags):
        self.id = id
        self.name = name
        self.description = description
        self.date = date
        # self.auditorium = auditorium
        # self.tags = tags


db.create_all()


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
@app.route('/admin/add-event', methods=['GET', 'POST'])
# def add_event(event):
#     db.session.add(event)
#     db.session.commit()
def add_event():
    if request.method == 'POST':
        #if not request.form['name']:
            # dodac wyjatek jak nie przekazany parametr name + inne (albo w formularzu)
        print(request.form['id'])
        print(request.form['name'])
        print(request.form['desc'])
        print(request.form['date'])
        data = datetime.datetime(*[int(v) for v in request.form['date'].replace('T', '-').replace(':', '-').split('-')])
        event = Event(id=request.form['id'], name=request.form['name'], description=request.form['desc'],
                      date=data)
        db.session.add(event)
                             #, request.form['auditorium'],
                             # request.form['tags']))
        db.session.commit()
        return redirect(url_for('get_all_event'))
    return render_template('add_event.html')


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

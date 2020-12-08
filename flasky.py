
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "const"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQlALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class users(db.Model):
    _id =  db.Column('id', db.Integer ,primary_key = True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    color = db.Column(db.String(15))
    location = db.Column(db.String)

    def __init__(self, name, age, color, location):
        self.name = name
        self.age = age
        self.color = color
        self.location = location

@app.route('/')
def home():
    re
    if len(session) == 0:
        flash("Welcome please sign in")
    return render_template("index.html")


@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/login', methods=["POST", "GET"])
def login():

    if "name" in session:
        return redirect(url_for("user"))
    elif request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        name = request.form["name"]
        session['name'] = name
        return redirect(url_for('login'))


@app.route('/logout', methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route('/user', methods=["POST", "GET"])
def user():

    if request.method == "POST":
        session['age'] = request.form['age']
        session['color'] = request.form['color']
        session['location'] = request.form['location']
        db.session.add(users(name=session['name'], age=session['age'], color=session['color'], location=session['location']))
        db.session.commit()
        print(users.query.all())
        return redirect(url_for('user'))
    elif request.method == "GET":
        found_user = users.query.filter_by(name = session['name']).first()
        if found_user is not None:
            session['age'] = found_user.age
            session['color'] = found_user.color
            session['location'] = found_user.location
            return render_template("user.html", user=session['name'], form=False, age=session['age'], color=session['color'], location=session['location'])
        else:
            flash("you are not signed in")
            return render_template("user.html", user=session['name'], form=True)

@app.route('/edit')
def edit():
    users.query.filter_by(name= session['name']).delete()
    db.session.commit()
    return render_template("user.html", user=session['name'], form=True)

@app.route('/delete', methods=['GET'])
def delete():
    users.query.filter_by(name=session['name']).delete()
    db.session.commit()
    session.clear()
    flash("account Deleted")
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    return render_template("admin.html", accounts=users.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


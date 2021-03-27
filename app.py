from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import flask_sqlalchemy

app = Flask(__name__)
app.secret_key = "key"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = flask_sqlalchemy.SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __repre__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login Successful!")

        return  redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "Get"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("Not logged in!")
        return redirect(url_for("login"))

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        session.pop("email", None)
        flash(f"Logged out {user}!", "info")
    return redirect(url_for("login"))

# Run flask app on localhost
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

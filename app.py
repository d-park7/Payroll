from flask import Flask, jsonify, redirect, url_for, render_template, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "PAYROLL"
app.permanent_session_lifetime = timedelta(minutes=30)

session = dict()

@app.route('/home', methods=["POST", "GET"])
def home():
    # If searching for employee, fetch data, otherwise load page
    if request.method == "POST":
        return f'<h1>Fetch employee id</h1>'
    else:
        return render_template('home.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    # If searching for employee, fetch data, otherwise load page
    if request.method == "POST":
        user = request.form["eid"]
        session['user'] = user
        return redirect(url_for("home"))
    else:
        return render_template('login.html')

# When user logs out, clear session data and redirect to login page
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for("login"))

# Run flask app on localhost
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
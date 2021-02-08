from flask import Flask, jsonify, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/test')
# def test():
#     return redirect(url_for("home", name="admin!", content=['apple', 'orange']))

# Run flask app on localhost
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
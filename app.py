from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Welcome to docker! If you got this far, congratulations</h1>'

# Run flask app on localhost
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
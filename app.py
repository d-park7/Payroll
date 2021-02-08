from flask import Flask, jsonify, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():

    # If searching for employee, fetch data, otherwise load page
    if request.method == "POST":
        employee_id = request.form['employee_id']
        return redirect('test')
    else:
        return render_template('home.html')


@app.route('/test')
def test():
    return f'<h1>Test page here</h1>'

# Run flask app on localhost
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
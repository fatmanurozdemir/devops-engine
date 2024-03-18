from flask import Flask, render_template, request, flash, redirect, url_for, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import requests
import os

app = Flask(__name__)
app.secret_key = 'thisisjustarandomstring'

# Initialize a counter metric for HTTP requests
http_requests_counter = Counter('http_requests_total', 'Total HTTP Requests', ['endpoint'])

@app.route('/', methods=['POST', 'GET'])
def index():
    # Increment the requests counter for the index endpoint
    http_requests_counter.labels(endpoint='/').inc()

    if request.method == "POST":
        if request.form['submit_button'] == 'Test connection':
            ret = os.system('ping welcome-service -w 1')
            if ret == 0:
                flash('The test was successful', "green")
                return redirect(url_for("test"))
            else:
                flash('The test failed. Welcome-service is not UP', "red")
                return redirect(url_for("index"))

        elif request.form['submit_button'] == 'Reset':
            return redirect(url_for("index"))
        else:
            pass
    return render_template('index.html')

@app.route('/test', methods=['POST', 'GET'])
def test():
    # Increment the requests counter for the test endpoint
    http_requests_counter.labels(endpoint='/test').inc()

    if request.method == "POST":
        if request.form['submit_button'] == 'Reset':
            return redirect(url_for("index"))
        elif request.form['submit_button'] == 'Get Message':
            data = requests.get('http://welcome-service:5051').json()
            flash(str(data), "green")
            return redirect(url_for('test'))
        else:
            pass
    return render_template('test_service.html')

# Route to expose Prometheus metrics
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    # Start Flask application
    app.run(debug=True, port=5050, host="0.0.0.0")

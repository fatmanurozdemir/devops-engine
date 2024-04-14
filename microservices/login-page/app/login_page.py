from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            warning_message = 'Please provide username and password'
            return render_template('login.html', warning_message=warning_message), 400
        # Check credentials (in a real application, you'd compare against a database)
        elif username == 'admin' and password == 'password':
            return redirect(url_for('success'))
        else:
            warning_message = 'Invalid username and password'
            return render_template('login.html', warning_message=warning_message), 400
    else:
        return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
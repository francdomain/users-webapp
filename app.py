from flask import Flask, render_template, request, redirect, session, flash
import json
import secrets

app = Flask(__name__)

# app.secret_key = 'your-secret-key'  # Replace with a secret key
app.secret_key = secrets.token_hex(16)  # Generate a 32-character random hexadecimal key


# Load users from JSON file (you can use a database instead)
with open('users.json', 'r') as file:
    users = json.load(file)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            users[username] = password
            with open('users.json', 'w') as file:
                json.dump(users, file)
            flash('Account created successfully!', 'success')
            return redirect('/login')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect('/login')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)

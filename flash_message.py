from flask import Flask, redirect, url_for, request,render_template, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key='mango'
# session to store permanently
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def admin():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        # setting session permanent as defined above
        session.permanent = True
        session['user'] = user
        flash('Login Succesful!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already Logged In')
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', user=user)
    else:
       flash('You are not logged in')
       return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash('You have been logged out,', 'info')
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__== '__main__':
    app.run()
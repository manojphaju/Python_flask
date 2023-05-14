from flask import Flask, redirect, url_for, request,render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='mango'
# session to store permanently
app.permanent_session_lifetime = timedelta(minutes=5)
# db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def admin():
    return render_template('index.html')

@app.route("/view")
def view():
    return render_template('view.html', values=users.query.all())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        # setting session permanent as defined above
        session.permanent = True
        session['user'] = user

        found_user = users.query.filter_by(name=user).first()
        # for delete user
        # found_user = users.query.filter_by(name=user).delete()
        # for user in found_user:
        #     user.delete()
        if found_user:
            session['email'] = found_user.email
            
        else:
            usr = users(user, '')
            db.session.add(usr)
            db.session.commit()

        flash('Login Succesful!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already Logged In')
            return redirect(url_for('user'))
        return render_template('login.html')

@app.route('/user', methods=["POST", "GET"])
def user():
    email = None
    if 'user' in session:
        user = session['user']

        if request.method == 'POST':
            email=request.form['email']
            session['email']=email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash('Email was saved')
        else:
            if 'email' in session:
                email = session['email']

        return render_template('user.html', email=email)
    else:
       flash('You are not logged in')
       return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash('You have been logged out,', 'info')
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__== '__main__':
    db.create_all()
    app.run()
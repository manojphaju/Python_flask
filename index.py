from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
    # return 'Hello from Flask'
    return render_template('index.html')

# @app.route('/<name>')
# def home(name):
#     return f'Hello {name}'

@app.route('/admin')
def admin():
    return redirect(url_for('home', name='admin!'))

# @app.route('/<name>')
# def content(name):
#     return render_template('index.html', content=name)

# @app.route('/<name>')
# def content(name):
#     return render_template('index.html', content=['apple','ball','cat'])

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    else:
        return render_template('login.html')

@app.route('/<usr>')
def user(usr):
    return f'<h1>hello {usr}</h1>'

if __name__== '__main__':
    app.run()
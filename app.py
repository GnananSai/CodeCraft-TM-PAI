from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, get_flashed_messages
from database import load_login_info, get_pass, register

app = Flask(__name__)


@app.route('/')
def hello_world():
  return render_template('landing.html')

@app.route("/loginpage")
def loginpage():
  return render_template("loginpage.html")

@app.route("/<username>")
def home(username):
  return render_template('homepage.html',username = username)

@app.route("/<username>/dashboard")
def dashboard(username):
  return render_template('dashboard.html', username=username)

@app.route("/<username>/community")
def community(username):
  return render_template('community.html', username=username)

@app.route("/<username>/community", methods=['post'])
def posted(username):
  data = request.form
  post = data['post']
  return render_template('community.html', username=username , msg="Posted succesfully", post = post)

@app.route("/<username>/focus-session")
def focus(username):
  return render_template('focus-session.html', username=username)

@app.route("/login", methods=['post'])
def login():
  data = request.form
  username = data['username']
  password = data['password']
  real = get_pass(username)
  if(real==None):
    error = "User Not found"
  elif (password == real):
    print("passwords match")
    return redirect(url_for('home', username=username))
  else:
    print("passwords dont match")
    error = "Incorrect Password"
  return render_template('loginpage.html', msg=error)

@app.route("/register", methods=['post'])
def register_page():
  data = request.form
  email = data['email']
  username = data['username']
  password = data['password']
  confirm = data['confirm']
  if(confirm==password):
    register(username, password, email)
    return render_template('success.html')
  else:
    return render_template('fail.html')
    
@app.route("/courses")
def courses():
  return render_template('courses.html')

@app.route("/<username>/mutherfucker")
def mutherfucker(username):
  return render_template('courses.html', username=username)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, get_flashed_messages
from database import load_login_info, get_pass, register

app = Flask(__name__)


@app.route('/')
def hello_world():
  return render_template('landing.html')

@app.route("/loginpage")
def loginpage():
  return render_template("loginpage.html")


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
    return render_template('success.html')
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
    


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

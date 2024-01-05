from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, get_flashed_messages
from database import load_login_info, get_pass, register, get_post, store_post, finish_course, get_user_course
from recommend import recommend

app = Flask(__name__)


@app.route('/')
def hello_world():
  return render_template('landing.html')

@app.route("/loginpage")
def loginpage():
  return render_template("loginpage.html")

@app.route("/<username>")
def home(username):
  recent = get_user_course(username=username)
  print(recent)
  courses = recommend(recent)
  return render_template('homepage.html',username = username, courses= courses, recent = recent)

@app.route("/<username>/dashboard")
def dashboard(username):
  return render_template('dashboard.html', username=username)

@app.route("/<username>/community")
def community(username):
  data=get_post()
  return render_template('community.html', username=username, data=data)

@app.route("/<username>/community", methods=['post'])
def posted(username):
  fufu = request.form
  post = fufu['post']
  store_post(username=username, content=post)
  data= get_post()
  return render_template('community.html', username=username , msg="Posted succesfully", post = post, data= data)

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
  users = load_login_info()
  counter=False
  for user in users:
    if(user['username']==username):
      counter=True
      break
  password = data['password']
  confirm = data['confirm']
  if(counter):
    return render_template('loginpage.html', msg="User already exists")
  if(confirm==password):
    register(username, password, email)
    return render_template('loginpage.html', msg="Register Succesfull")
  else:
    return render_template('loginpage.html', msg="Passwords do not match")
    
@app.route("/courses")
def courses():
  return render_template('courses.html')

@app.route("/<username>/ucourses")
def ucourses(username):
  return render_template('courses.html', username=username)

@app.route("/<username>/utilities")
def utilities(username):
  return render_template('utilities.html', username=username)

@app.route("/<username>/<course_name>")
def course_page(username, course_name):
  return render_template('coursepage.html', username = username, course_name=course_name)
def enrolled(username, course_name):
  finish_course(username=username, course_name=course_name)
  return render_template('coursepage.html',username= username, msg="Finished Successfully", course_name=course_name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, get_flashed_messages
from database import load_login_info, get_pass, register, get_post, store_post, finish_course, get_user_course, store_task, get_task
from recommend import recommend

app = Flask(__name__)


@app.route('/')
def hello_world():
  try:
    return render_template('landing.html')
  except:
    return render_template('error.html')

@app.route("/loginpage")
def loginpage():
  try:
    return render_template("loginpage.html")
  except:
    return render_template('error.html')

@app.route("/<username>")
def home(username):
  try:
    recent = get_user_course(username=username)
    courses = recommend(recent)
    return render_template('homepage.html',username = username, courses= courses, recent = recent)
  except:
    return render_template('error.html')

@app.route("/<username>/mycourses")
def mycourses(username):
  return render_template('mycourses.html', username=username)


@app.route("/<username>/dashboard")
def dashboard(username):
  try:
    return render_template('dashboard.html', username=username)
  except:
    return render_template('error.html')

@app.route("/<username>/community")
def community(username):
  try: 
    data=get_post()
    return render_template('community.html', username=username, data=data)
  except:
    return render_template('error.html')
  
@app.route("/<username>/community", methods=['post'])
def posted(username):
  try: 
    fufu = request.form
    post = fufu['post']
    store_post(username=username, content=post)
    data= get_post()
    return render_template('community.html', username=username , msg="Posted succesfully", post = post, data= data)
  except:
    return render_template('error.html')

@app.route("/<username>/focus-session")
def focus(username):
  try: 
    return render_template('focus-session.html', username=username)
  except:
    return render_template('error.html')

@app.route("/login", methods=['post'])
def login():
  try: 
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
  except:
    return render_template('error.html')

@app.route("/register", methods=['post'])
def register_page():
  try:
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
  except:
    return render_template('error.html')
    
@app.route("/courses")
def courses():
  try:
    return render_template('courses.html')
  except:
    return render_template('error.html')
  

@app.route("/<username>/ucourses")
def ucourses(username):
  try: 
    return render_template('courses.html', username=username)
  except:
    return render_template('error.html')

@app.route("/<username>/utilities", methods= ['post'])
def utilities(username, newtask):
  try: 
    if(newtask):
      store_task(newtask, username=username)
    else:
      tasks = get_task(username=username)
      return render_template('utilities.html', username=username, tasks= tasks)
  except:
    return render_template('error.html')

@app.route("/<username>/<course_name>")
def course_page(username, course_name):
  try:
    return render_template('coursepage.html', username = username, course_name=course_name)
  except:
    return render_template('error.html')


@app.route("/<username>/<course_name>/confirmation")
def enrolled(username, course_name):
  try:
    finish_course(username=username, course_name=course_name)
    return render_template('coursepage.html',username= username, msg="Finished Successfully", course_name=course_name)
  except:
    return render_template('error.html')
  

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)

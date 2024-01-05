from sqlalchemy import create_engine, text
import os
import time
from datetime import datetime

f = '%Y-%m-%d %H:%M:%S'
db_connection_string = "mysql+pymysql://2CKpNXaNba8Kkqc.root:vXvZuAtHltAJ9J1R@gateway01.ap-southeast-1.prod.aws.tidbcloud.com/test?charset=utf8mb4"

engine = create_engine(
  db_connection_string,
  connect_args={
    'ssl':{
      "ca": "isrgrootx1.pem",
    }
  }
)

def load_login_info():
  with engine.connect() as conn:
    result = conn.execute(text("select id, username, pw from login_info"))
    result_dict = []
    for row in result:
      result_dict.append(row._mapping)
  return(result_dict)

def get_pass(user):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT pw FROM login_info WHERE username = :u"),dict(u=user))
    dumb = []
    for row in result:
      dumb.append(row._mapping)
    try:
      return (dumb[0].get('pw'))
    except:
      return None

def get_course_data():
  with engine.connect() as conn:
    result = conn.execute(text("select * from course_details"))
    result_dict = []
    for row in result:
      result_dict.append(row._mapping)
  return (result_dict)  

def register(user, pw, email):
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO login_info (username, pw, email) VALUES (:u, :p, :e)"),dict(u=user, p=pw, e=email))  
    conn.commit()




def store_post(content, username):
  now=time.localtime()
  t=time.strftime(f, now)
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO community (username,content,post_time) VALUES (:u, :p, :e)"),dict(u=username, p=content, e=t))  
    conn.commit()

def get_post():
  with engine.connect() as conn:
    result = conn.execute(text("select * from community order by post_time desc limit 5"))
    result_dict = []
    for row in result:
      result_dict.append(row._mapping)
  return (result_dict)  

def finish_course(username, course_name):
  now=time.localtime()
  t=time.strftime(f, now)
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO user_courses (username,course_name,completion_time) VALUES (:u, :p, :e)"),dict(u=username, p=course_name, e=t))  
    conn.commit()


def get_user_course(username):
  with engine.connect() as conn:
    result = conn.execute(text("select course_name from user_courses where username=:u order by completion_time desc limit 1;"),dict(u=username))
    dumb = []
    for row in result:
      dumb.append(row._mapping)
    try:
      print(dumb[0].get('course_name'))
      return (dumb[0].get('course_name'))
    except:
      return "Classical Mechanics"
    

#finish_course("admin", "Circuits and Electronics")
finish_course("admin1", "Intoduction to Control System Design")

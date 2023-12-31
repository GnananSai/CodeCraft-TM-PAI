from sqlalchemy import create_engine, text
import os

db_connection_string = DB_CONNECTION_STRING

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
    return (dumb[0].get('pw'))

def register(user, pw, email):
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO login_info (username, pw, email) VALUES (:u, :p, :e)"),dict(u=user, p=pw, e=email))  
    conn.commit()

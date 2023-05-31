from sqlalchemy import create_engine, text
import os

engine = create_engine(os.environ.get('DB_CONN_STRING'), 
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)

with engine.connect() as conn:
  result = conn.execute(text("select * from users"))
  print(result.all())


def get_users_from_db():
    with engine.connect() as conn:
        users = []
        rows = conn.execute(text("SELECT * FROM users"))  # convert the string into a SQL expression
        for row in rows:
          users.append(row)
    return users


def load_user_from_db(username):
  with engine.connect() as conn:
    user = conn.execute(
      text("SELECT * FROM users WHERE username = :val"),
       { "val":username }
    ).all()
    if result:  # if the list is not empty
            return result[0]
    else:
        return None

def add_user_to_db(user):
  with engine.connect() as conn:
    query = text("INSERT INTO users (username, fname, sname, email, password_hash, journal) VALUES (:username, :fname, :sname, :email, :password_hash, :journal)")
    
    conn.execute(query, 
                 username=user.username, 
                 fname=user.fname, 
                 sname=user.sname, 
                 email=user.email, 
                 password_hash=user.password_hash, 
                 jouranl=user.journal)
    
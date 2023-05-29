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


def load_user_from_db(id):
  with engine.connect() as conn:
    user = conn.execute(
      text("SELECT * FROM users WHERE id = :val"),
       { "val":id }
    ).all()
    return user[0]
  
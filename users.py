from db import db
from sqlalchemy import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = text("SELECT id, password from users where username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            session["id"] = user[0]
            return True
        else:
            return False

def signup(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("insert into users (username, password, tier) values (:username,:password,0)")
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["id"]

def get_id():
    return session.get("id",0)

def is_admin():
    id = get_id()
    if id > 0:
        sql = text("""SELECT users.tier 
                from users 
                where users.id=:id""")
        result = db.session.execute(sql, {"id":id})
        tier = result.fetchone()
        if tier[0] == 1:
          return True
    return False
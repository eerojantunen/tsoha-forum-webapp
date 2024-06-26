from db import db
from sqlalchemy import text
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

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
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def signup(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""insert into users (username, password, tier)
                    values (:username,:password,0)
                   returning id""")
        result = db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    if result.fetchone()[0] == 1:
        sql = text("""update users 
                   set tier = 1
                   where users.id = 1
                   """)
        result = db.session.execute(sql)
        db.session.commit()
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

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
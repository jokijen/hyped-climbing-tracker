import secrets
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def user_login(username, password):
    sql = "SELECT id, password, administrator FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["admin"] = user.administrator
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False
        

def user_logout():
    session.clear()


def register_user(username, email, password): 
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,email,password) VALUES (:username,:email,:password)"
        db.session.execute(text(sql), {"username":username, "email":email, "password":hash_value})
        db.session.commit()
    except:
        return False
    return user_login(username, password)


def user_id():
    return session.get("user_id")


def is_admin():
    return session.get("admin", False)

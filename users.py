import re
import secrets
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def is_valid_password(password): 
    if len(password) < 8: # password must be min. 8 characters long 
        return False
    if not re.search(r"\d", password): # must contain at least one number
        return False
    return True


def register_user(username, email, password): 
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
        db.session.execute(text(sql), {"username":username, "email":email, "password":hash_value})
        db.session.commit()
    except:
        return False
    return user_login(username, password)


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


def validate_password(user_id, password): # validate old password for changing the password
    sql = "SELECT password FROM users WHERE id=:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    old_pass = result.fetchone()
    if check_password_hash(old_pass.password, password):
        return True
    return False


def change_password(user_id, password):
    hash_value = generate_password_hash(password)
    try: 
        sql = "UPDATE users SET password=:hash_value WHERE id=:user_id"
        db.session.execute(text(sql), {"hash_value":hash_value, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False


def user_logout():
    session.clear()


def user_id():
    return session.get("user_id")


def get_user_info(user_id):
    sql = """
    SELECT id, username, email, 
    DATE(created_at) AS creation_date, 
    TO_CHAR(created_at, 'HH24:MI') AS creation_time 
    FROM users 
    WHERE id=:user_id"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    user_info = result.fetchone()
    return user_info


def is_admin():
    return session.get("admin", False)


def is_suspended(username):
    sql = "SELECT suspended FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user[0]: 
        return True
    return False

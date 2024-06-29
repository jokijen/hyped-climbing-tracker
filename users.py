"""
This module defines the functions related to handling users
for the Hyped app web application.
"""
import re
import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db


def is_valid_password(password):
    """Returns boolean for whether the password the user is trying to set is valid"""
    if len(password) < 8: # password must be min. 8 characters long
        return False
    if not re.search(r"\d", password): # must contain at least one number
        return False
    return True


def register_user(username, email, password):
    """Registers a new user and logs them in"""
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
        db.session.execute(text(sql), {"username":username, "email":email, "password":hash_value})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return user_login(username, password)


def user_login(username, password):
    """Logs the user in"""
    sql = "SELECT id, password, administrator FROM users WHERE username = :username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["admin"] = user.administrator
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False


def validate_password(user_id, password):
    """Validates the old password when changing the password"""
    sql = "SELECT password FROM users WHERE id = :user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    old_pass = result.fetchone()
    if check_password_hash(old_pass.password, password):
        return True
    return False


def change_password(user_id, password):
    """Changes the user's password"""
    hash_value = generate_password_hash(password)
    try:
        sql = "UPDATE users SET password = :hash_value WHERE id = :user_id"
        db.session.execute(text(sql), {"hash_value":hash_value, "user_id":user_id})
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def user_logout():
    """Logs the user out bu clearing the session"""
    session.clear()


def get_user_id():
    """Returns the user's id"""
    return session.get("user_id")


def get_user_info(user_id):
    """Returns user information"""
    sql = """
    SELECT id, username, email, 
    DATE(created_at) AS creation_date, 
    TO_CHAR(created_at, 'HH24:MI') AS creation_time 
    FROM users 
    WHERE id = :user_id"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    user_info = result.fetchone()
    return user_info


def is_admin():
    """Returns boolean for the users admin status"""
    return session.get("admin", False)


def is_suspended(username):
    """Returns boolean on if the user is suspended"""
    try:
        sql = "SELECT suspended FROM users WHERE username = :username"
        result = db.session.execute(text(sql), {"username":username})
        user = result.fetchone()
        if user[0]:
            return True
        return False
    except Exception as e: # If user does not exist or other error
        print(e)
        return False


def all_free_non_admins():
    """Returns all non-suspendednon-admin users' id and username"""
    sql = """
    SELECT id, username
    FROM users
    WHERE administrator = FALSE
    AND suspended = FALSE
    ORDER BY username"""
    result = db.session.execute(text(sql))
    free_non_admins = result.fetchall()
    return free_non_admins


def all_suspended_non_admins():
    """Returns all suspended non-admin users' id and username"""
    sql = """
    SELECT id, username
    FROM users
    WHERE administrator = FALSE
    AND suspended = TRUE
    ORDER BY username"""
    result = db.session.execute(text(sql))
    suspended_non_admins = result.fetchall()
    return suspended_non_admins


def suspend_user_by_id(user_id):
    """Suspends a user"""
    try:
        sql = "UPDATE users SET suspended = TRUE WHERE id = :user_id"
        db.session.execute(text(sql), {"user_id":user_id})
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def free_user_by_id(user_id):
    """Frees a user from suspension"""
    try:
        sql = "UPDATE users SET suspended = FALSE WHERE id = :user_id"
        db.session.execute(text(sql), {"user_id":user_id})
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

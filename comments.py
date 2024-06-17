from db import db
from sqlalchemy import text


def get_comments_for_climb_id(id): # all comments for that climb
    sql = """
    SELECT c.id, c.user_id, u.username, c.content, 
    DATE(c.created_at) AS creation_date, 
    TO_CHAR(c.created_at, 'HH24:MI') AS creation_time 
    FROM users u, comments c
    WHERE c.climb_id=:id 
    AND c.user_id=u.id
    AND c.deleted IS NOT TRUE
    ORDER BY c.created_at DESC"""
    result = db.session.execute(text(sql), {"id":id})
    comments_for_climb = result.fetchall()
    return comments_for_climb


def get_comment_for_comment_id(id): # all comments for that climb
    sql = """
    SELECT id, user_id, climb_id, content, deleted
    FROM comments
    WHERE id=:id""" 
    result = db.session.execute(text(sql), {"id":id})
    comment = result.fetchone()
    return comment


def add_comment(user_id, climb_id, content):
    try:
        sql = "INSERT INTO comments (user_id, climb_id, content) VALUES (:user_id, :climb_id, :content)"
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id, "content":content})
        db.session.commit()
    except:
        return False
    return True


def delete_comment_using_id(id):
    try:
        sql = "UPDATE comments SET deleted=TRUE WHERE id=:id"
        db.session.execute(text(sql), {"id":id})
        db.session.commit()
    except:
        return False
    return True
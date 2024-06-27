"""
This module defines the functions related to handling comments of climbs
for the Hyped app web application.
"""
from sqlalchemy import text
from db import db


def get_comments_for_climb_id(climb_id):
    """Returns all comments for that a climb by climb's id"""
    sql = """
    SELECT c.id, c.user_id, u.username, c.content, 
    DATE(c.created_at) AS creation_date, 
    TO_CHAR(c.created_at, 'HH24:MI') AS creation_time 
    FROM users u, comments c
    WHERE c.climb_id = :climb_id 
    AND c.user_id = u.id
    AND c.deleted IS NOT TRUE
    ORDER BY c.created_at DESC"""
    result = db.session.execute(text(sql), {"climb_id":climb_id})
    comments_for_climb = result.fetchall()
    return comments_for_climb


def get_comment_for_comment_id(comment_id):
    """Get comment by comment id"""
    sql = """
    SELECT id, user_id, climb_id, content, deleted
    FROM comments
    WHERE id = :comment_id"""
    result = db.session.execute(text(sql), {"comment_id":comment_id})
    comment = result.fetchone()
    return comment


def add_comment(user_id, climb_id, content):
    """Add a new comment"""
    try:
        sql = """
        INSERT INTO comments (user_id, climb_id, content)
        VALUES (:user_id, :climb_id, :content)"""
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id, "content":content})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


def delete_comment_using_id(comment_id):
    """Delete comment by comment id"""
    try:
        sql = "UPDATE comments SET deleted = TRUE WHERE id = :comment_id"
        db.session.execute(text(sql), {"comment_id":comment_id})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

"""
This module defines the functions related to handling the tick-list
for the Hyped app web application.
"""
from sqlalchemy import text
from db import db


def get_ticklist(user_id):
    """Returns the contents of the user's tick-list incl. climbs and their crags"""
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by, t.created_at
    FROM climbs c, ticklist t, crags r
    WHERE t.climb_id = c.id 
    AND t.user_id = :user_id 
    AND c.crag_id = r.id
    AND t.deleted IS NOT TRUE
    ORDER BY t.created_at DESC"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    tick_list = result.fetchall()
    return tick_list


def is_on_ticklist(user_id, climb_id):
    """Returns boolean value for the climb being on the user's tick-list"""
    sql = """
    SELECT EXISTS (
    SELECT 1
    FROM ticklist 
    WHERE user_id = :user_id
    AND climb_id = :climb_id
    AND deleted IS NOT TRUE
    )"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    exists = result.fetchone()
    return exists[0]


def date_ticked(user_id, climb_id):
    """Returns date when the user added the climb to their tick-list"""
    sql = """
    SELECT DATE(created_at) AS creation_date
    FROM ticklist
    WHERE user_id = :user_id
    AND climb_id = :climb_id
    AND deleted IS NOT TRUE"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    tick_date = result.fetchone()
    if tick_date is None:
        return "-"
    return tick_date[0]


def times_on_ticklist(climb_id):
    """Returns how many times a climb has been ticked by users"""
    sql = "SELECT COUNT(*) FROM ticklist WHERE climb_id = :climb_id AND deleted IS NOT TRUE"
    result = db.session.execute(text(sql), {"climb_id":climb_id})
    tick_count = result.fetchone()
    return tick_count[0]


def add_climb_to_ticklist(user_id, climb_id):
    """Adds a crag to the user's favourite_crags"""
    try:
        sql = """
        INSERT INTO ticklist (user_id, climb_id)
        VALUES (:user_id, :climb_id)
        ON CONFLICT (user_id, climb_id) DO UPDATE
        SET deleted = FALSE, created_at = NOW()"""
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


def delete_from_ticklist(user_id, climb_id):
    """Marks a tick as deleted by user id and climb id"""
    try:
        sql = "UPDATE ticklist SET deleted = TRUE WHERE user_id = :user_id AND climb_id = :climb_id"
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

from db import db
from sqlalchemy import text


def get_ticklist(user_id):
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by, t.created_at
    FROM climbs c, ticklist t, crags r
    WHERE t.climb_id=c.id 
    AND t.user_id=:user_id 
    AND c.crag_id=r.id
    AND t.deleted IS NOT TRUE
    ORDER BY t.created_at DESC"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    tick_list = result.fetchall()
    return tick_list


def is_on_ticklist(user_id, climb_id):
    sql = """
    SELECT EXISTS (
    SELECT 1
    FROM ticklist 
    WHERE user_id=:user_id
    AND climb_id=:climb_id
    )"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    exists = result.fetchone()
    return exists[0]


def date_ticked(user_id, climb_id): 
    sql = "SELECT DATE(created_at) AS creation_date FROM ticklist WHERE user_id=:user_id AND climb_id=:climb_id"
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    tick_date = result.fetchone()
    if tick_date is None:
        return "-"
    return tick_date[0]


def times_on_ticklist(climb_id):
    sql = "SELECT COUNT(*) FROM ticklist WHERE climb_id=:climb_id"
    result = db.session.execute(text(sql), {"climb_id":climb_id})
    tick_count = result.fetchone()
    return tick_count[0]


def add_climb_to_ticklist(user_id, climb_id): # Adds a crag to the user's favourite_crags
    try:
        sql = """
        INSERT INTO ticklist (user_id, climb_id)
        VALUES (:user_id, :climb_id)"""
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
        db.session.commit()
    except: 
        return False
    return True


def delete_from_ticklist(user_id, climb_id):
    try: 
        sql = "UPDATE ticklist SET deleted=TRUE WHERE user_id=:user_id AND climb_id=:climb_id"
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
        db.session.commit()
    except:
        return False
    return True
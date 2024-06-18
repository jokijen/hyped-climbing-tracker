from db import db
from sqlalchemy import text


def get_sends_for_climb_id(id): # all sends of that climb
    sql = """
    SELECT u.username, s.send_date, s.send_type, s.review, s.rating
    FROM users u, sends s
    WHERE s.climb_id=:id 
    AND s.user_id=u.id
    AND s.deleted IS NOT TRUE
    ORDER BY s.send_date DESC"""
    result = db.session.execute(text(sql), {"id":id})
    sends_for_climb = result.fetchall()
    return sends_for_climb


def get_sends_for_user(user_id): 
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by, s.send_date, s.send_type, s.review, s.rating
    FROM climbs c, sends s, crags r
    WHERE s.climb_id=c.id 
    AND s.user_id=:user_id 
    AND c.crag_id=r.id
    AND s.deleted IS NOT TRUE
    ORDER BY s.send_date DESC"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    logged_sends = result.fetchall()
    return logged_sends


def add_send(user_id, climb_id, send_date, send_type, review, rating):
    try:
        sql = """
        INSERT INTO sends(user_id, climb_id, send_date, send_type, review, rating)
        VALUES (:user_id, :climb_id, :send_date, :send_type, :review, :rating)"""
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id, "send_date":send_date, "send_type":send_type, "review":review, "rating":rating})
        db.session.commit()
    except:
        return False
    return True
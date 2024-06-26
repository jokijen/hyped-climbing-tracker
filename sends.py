from db import db
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound


def get_sends_for_climb_id(climb_id): # all sends of that climb
    sql = """
    SELECT u.username, s.send_date, s.send_type, s.review, s.rating
    FROM users u, sends s
    WHERE s.climb_id = :climb_id 
    AND s.user_id = u.id
    AND s.deleted IS NOT TRUE
    ORDER BY s.send_date DESC"""
    result = db.session.execute(text(sql), {"climb_id":climb_id})
    sends_for_climb = result.fetchall()
    return sends_for_climb


def get_sends_for_user(user_id): 
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by, s.send_date, s.send_type, s.review, s.rating
    FROM climbs c, sends s, crags r
    WHERE s.climb_id = c.id 
    AND s.user_id = :user_id 
    AND c.crag_id = r.id
    AND s.deleted IS NOT TRUE
    ORDER BY s.send_date DESC"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    logged_sends = result.fetchall()
    return logged_sends


def get_latest_sends():
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, s.send_date, s.send_type, s.review, s.rating, u.username
    FROM climbs c
    JOIN sends s ON s.climb_id = c.id
    JOIN crags r ON c.crag_id = r.id
    JOIN users u ON s.user_id = u.id
    WHERE s.deleted IS NOT TRUE
    ORDER BY s.send_date DESC
    LIMIT 5"""
    result = db.session.execute(text(sql))
    latest_sends = result.fetchall()
    return latest_sends


def is_sent(user_id, climb_id):
    sql = """
    SELECT EXISTS (
    SELECT 1
    FROM sends 
    WHERE user_id = :user_id
    AND climb_id = :climb_id
    AND deleted IS NOT TRUE
    )"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    exists = result.fetchone()[0]
    return exists


def date_sent(user_id, climb_id):
    sql = """
    SELECT send_date 
    FROM sends 
    WHERE user_id = :user_id 
    AND climb_id = :climb_id
    AND deleted IS NOT TRUE"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    send_date = result.fetchone()
    if send_date is None:
        return "-"
    return send_date[0]


def average_rating(climb_id): 
    sql = "SELECT AVG(rating) FROM sends WHERE climb_id = :climb_id AND deleted <> TRUE"
    result = db.session.execute(text(sql), {"climb_id":climb_id})
    avg = result.fetchone()
    if avg[0] is None:
        return "-"
    return f"{avg[0]:.1f}"


def add_send(user_id, climb_id, send_date, send_type, review, rating):
    try:
        sql = """
        INSERT INTO sends(user_id, climb_id, send_date, send_type, review, rating)
        VALUES (:user_id, :climb_id, :send_date, :send_type, :review, :rating)
        ON CONFLICT (user_id, climb_id) DO UPDATE
        SET deleted = FALSE, 
            created_at = NOW(), 
            user_id = :user_id, 
            climb_id = :climb_id, 
            send_date = :send_date, 
            send_type = :send_type, 
            review = :review, 
            rating = :rating"""
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id, "send_date":send_date, "send_type":send_type, "review":review, "rating":rating})
        db.session.commit()
    except:
        return False
    return True


def get_send_details(user_id, climb_id):
    sql = """
    SELECT send_date, send_type, review, rating
    FROM sends 
    WHERE climb_id = :climb_id 
    AND user_id = :user_id
    AND deleted IS NOT TRUE"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    send_details = result.fetchone()
    return send_details


def delete_send(user_id, climb_id):
    try:
        sql = "UPDATE sends SET deleted = TRUE WHERE user_id = :user_id AND climb_id = :climb_id"
        db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
        db.session.commit()
    except:
        return False
    return True
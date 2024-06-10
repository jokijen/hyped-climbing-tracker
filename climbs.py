from db import db
from sqlalchemy import text


def get_all_climbs():
    sql = "SELECT * FROM climbs ORDER BY climb_name"
    result = db.session.execute(text(sql))
    all_climbs = result.fetchall()
    return all_climbs


def get_climb(id):
    sql = "SELECT * FROM climbs WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    climb_info = result.fetchone()
    return climb_info


def get_climbs_by_crag_id(crag_id):
    sql = "SELECT * FROM climbs WHERE crag_id=:crag_id"
    result = db.session.execute(text(sql), {"crag_id":crag_id})
    climbs_at_crag = result.fetchall()
    return climbs_at_crag


def get_comments_for_climb_id(id): # all comments for that climb
    sql = """
    SELECT u.username, c.comment, c.created_at
    FROM users u, comments c
    WHERE c.climb_id=:id 
    AND c.user_id=u.id
    ORDER BY c.created_at DESC"""
    result = db.session.execute(text(sql), {"id":id})
    comments_for_climb = result.fetchall()
    return comments_for_climb


def get_sends_for_climb_id(id): # all sends of that climb
    sql = """
    SELECT u.username, c.send_date, c.send_type, c.review, c.rating
    FROM users u, sends c
    WHERE c.climb_id=:id 
    AND c.user_id=u.id
    ORDER BY c.send_date DESC"""
    result = db.session.execute(text(sql), {"id":id})
    sends_for_climb = result.fetchall()
    return sends_for_climb


def add_climb(name, difficulty, type, description, created_by): # not finished/tested
    sql = """
    INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, created_by)
    VALUES (:name, :difficulty, :type, :description, :created_by)"""
    db.session.execute(text(sql), {"name":name, "difficulty":difficulty, "type":type, "description":description, "created_by":created_by})
    db.session.commit()
    return True


def search_climbs(query): 
    q = query.lower()
    sql = """
    SELECT * FROM climbs 
    WHERE LOWER(climb_name) LIKE :q 
    OR LOWER(difficulty) LIKE :q
    OR LOWER(climb_type) LIKE :q
    OR LOWER(climb_description) LIKE :q
    OR LOWER(created_by) LIKE :q"""
    result = db.session.execute(text(sql), {"q":"%"+q+"%"})
    found_crags = result.fetchall()
    return found_crags
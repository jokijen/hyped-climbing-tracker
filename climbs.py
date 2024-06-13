from db import db
from sqlalchemy import text


def get_all_climbs():
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id=r.id
    ORDER BY climb_name"""
    result = db.session.execute(text(sql))
    all_climbs = result.fetchall()
    return all_climbs


def get_climb(id):
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id=r.id 
    AND c.id=:id"""
    result = db.session.execute(text(sql), {"id":id})
    climb_info = result.fetchone()
    return climb_info


def get_climbs_by_crag_id(crag_id):
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id=r.id 
    AND c.crag_id=:crag_id"""
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


def get_ticklist(user_id):
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.created_by, t.created_at
    FROM climbs c, ticklist t, crags r
    WHERE t.climb_id=c.id 
    AND t.user_id=:user_id 
    AND c.crag_id=r.id
    ORDER BY t.created_at DESC"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    tick_list = result.fetchall()
    return tick_list


def get_sends(user_id): 
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.created_by, s.send_date, s.send_type, s.review, s.rating
    FROM climbs c, sends s, crags r
    WHERE s.climb_id=c.id 
    AND s.user_id=:user_id 
    AND c.crag_id=r.id
    ORDER BY s.send_date DESC"""
    result = db.session.execute(text(sql), {"user_id":user_id})
    logged_sends = result.fetchall()
    print(logged_sends)
    return logged_sends


def add_new_climb(name, difficulty, type, description, crag_id, created_by): # not finished/tested
    sql = """
    INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, created_by)
    VALUES (:name, :difficulty, :type, :description, :crag_id, :created_by)"""
    db.session.execute(text(sql), {"name":name, "difficulty":difficulty, "type":type, "description":description, "crag_id":crag_id, "created_by":created_by})
    db.session.commit()
    return True


def search_climbs(query): 
    q = query.lower()
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.created_by 
    FROM climbs c 
    JOIN crags r ON c.crag_id=r.id
    WHERE (
    LOWER(c.climb_name) LIKE :q 
    OR LOWER(c.difficulty) LIKE :q
    OR LOWER(c.climb_type) LIKE :q
    OR LOWER(c.climb_description) LIKE :q
    OR LOWER(r.crag_name) LIKE :q
    OR LOWER(c.created_by) LIKE :q
    )
    ORDER BY c.climb_name
    """
    result = db.session.execute(text(sql), {"q":"%"+q+"%"})
    found_crags = result.fetchall()
    return found_crags
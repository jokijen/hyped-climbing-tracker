from db import db
from sqlalchemy import text
import random 


def get_all_climbs():
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id=r.id
    ORDER BY climb_name"""
    result = db.session.execute(text(sql))
    all_climbs = result.fetchall()
    return all_climbs


def get_climb(id):
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id=r.id 
    AND c.id=:id"""
    result = db.session.execute(text(sql), {"id":id})
    climb_info = result.fetchone()
    return climb_info


def get_climbs_by_crag_id(crag_id):
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id=r.id 
    AND c.crag_id=:crag_id"""
    result = db.session.execute(text(sql), {"crag_id":crag_id})
    climbs_at_crag = result.fetchall()
    return climbs_at_crag


def get_random_climb():
    sql = "SELECT id FROM climbs"
    result = db.session.execute(text(sql))
    all_ids = [row[0] for row in result.fetchall()]
    return random.choice(all_ids)


def add_new_climb(name, difficulty, type, description, crag_id, first_ascent, created_by): 
    try: 
        sql = """
        INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by)
        VALUES (:name, :difficulty, :type, :description, :crag_id, :first_ascent, :created_by)"""
        db.session.execute(text(sql), {"name":name, "difficulty":difficulty, "type":type, "description":description, "crag_id":crag_id, "first_ascent":first_ascent, "created_by":created_by})
        db.session.commit()
    except:
        return False
    return True


def is_sent(user_id, climb_id):
    sql = """
    SELECT EXISTS (
    SELECT 1
    FROM sends 
    WHERE user_id=:user_id
    AND climb_id=:climb_id
    )"""
    result = db.session.execute(text(sql), {"user_id":user_id, "climb_id":climb_id})
    exists = result.fetchone()[0]
    return exists


def search_climbs(query): # search shows more relevant results first
    q = query.lower()
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent 
    FROM climbs c 
    JOIN crags r ON c.crag_id=r.id
    WHERE (
    LOWER(c.climb_name) LIKE :q 
    OR LOWER(c.difficulty) LIKE :q
    OR LOWER(c.climb_type) LIKE :q
    OR LOWER(c.climb_description) LIKE :q
    OR LOWER(r.crag_name) LIKE :q
    OR LOWER(c.first_ascent) LIKE :q
    )
    ORDER BY 
    CASE
        WHEN LOWER(c.climb_name) LIKE :q THEN 1
        WHEN LOWER(c.difficulty) LIKE :q THEN 2
        WHEN LOWER(c.climb_type) LIKE :q THEN 3
        WHEN LOWER(c.climb_description) LIKE :q THEN 4
        WHEN LOWER(r.crag_name) LIKE :q THEN 5
        WHEN LOWER(c.first_ascent) LIKE :q THEN 6
        ELSE 7
    END
    """
    result = db.session.execute(text(sql), {"q":"%"+q+"%"})
    found_climbs = result.fetchall()
    return found_climbs
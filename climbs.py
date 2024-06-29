"""
This module defines the functions related to handling climbs
for the Hyped app web application.
"""
import random
from sqlalchemy import text
from db import db


def get_all_climbs():
    """Returns all climbs and their info (incl. their crag) in alphabetical order of climb"""
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id = r.id
    ORDER BY climb_name"""
    result = db.session.execute(text(sql))
    all_climbs = result.fetchall()
    return all_climbs


def get_climb(climb_id):
    """Returns information of a climb (incl. crag it is in) by the climb's id"""
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id = r.id 
    AND c.id = :climb_id"""
    result = db.session.execute(text(sql), {"climb_id":climb_id})
    climb_info = result.fetchone()
    return climb_info


def get_climbs_by_crag_id(crag_id):
    """Returns al climbs of a specific crag and their information"""
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent, c.created_by 
    FROM climbs c, crags r
    WHERE c.crag_id = r.id 
    AND c.crag_id = :crag_id"""
    result = db.session.execute(text(sql), {"crag_id":crag_id})
    climbs_at_crag = result.fetchall()
    return climbs_at_crag


def get_random_climb():
    """Returns a valid climb id from the database so that a random climb can be retrieved"""
    sql = "SELECT id FROM climbs"
    result = db.session.execute(text(sql))
    all_ids = [row[0] for row in result.fetchall()]
    return random.choice(all_ids)


def add_new_climb(name, difficulty, climb_type, description, crag_id, first_ascent, created_by):
    """Inserts a new climb into the database and returns its id"""
    try:
        sql = """
        INSERT INTO climbs (climb_name, difficulty, climb_type, climb_description, crag_id, first_ascent, created_by)
        VALUES (:name, :difficulty, :climb_type, :description, :crag_id, :first_ascent, :created_by)
        RETURNING id"""
        result = db.session.execute(text(sql), {
            "name":name,
            "difficulty":difficulty,
            "climb_type":climb_type,
            "description":description,
            "crag_id":crag_id,
            "first_ascent":first_ascent,
            "created_by":created_by
        })
        new_climb_id = result.fetchone()[0]
        db.session.commit()
    except Exception as e:
        print(e)
        return None
    return new_climb_id


def edit_climb(climb_id, climb_name, difficulty, climb_type, climb_description, first_ascent):
    try:
        sql = """
        UPDATE climbs
        SET climb_name = :climb_name,
            difficulty = :difficulty,
            climb_type = :climb_type,
            climb_description = :climb_description,
            first_ascent = :first_ascent
        WHERE id = :climb_id"""
        db.session.execute(text(sql), {
            "climb_name":climb_name,
            "difficulty":difficulty,
            "climb_type":climb_type,
            "climb_description":climb_description,
            "first_ascent":first_ascent,
            "climb_id":climb_id
        })
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


def search_climbs(query):
    """A search that shows more relevant results first"""
    q_lower = query.lower()
    sql = """
    SELECT c.id, c.climb_name, c.difficulty, c.climb_type, c.climb_description, c.crag_id, r.crag_name, c.first_ascent 
    FROM climbs c 
    JOIN crags r ON c.crag_id = r.id
    WHERE (
    LOWER(c.climb_name) LIKE :q_lower
    OR LOWER(c.difficulty) LIKE :q_lower
    OR LOWER(c.climb_type) LIKE :q_lower
    OR LOWER(c.climb_description) LIKE :q_lower
    OR LOWER(r.crag_name) LIKE :q_lower
    OR LOWER(c.first_ascent) LIKE :q_lower
    )
    ORDER BY 
    CASE
        WHEN LOWER(c.climb_name) LIKE :q_lower THEN 1
        WHEN LOWER(c.difficulty) LIKE :q_lower THEN 2
        WHEN LOWER(c.climb_type) LIKE :q_lower THEN 3
        WHEN LOWER(c.climb_description) LIKE :q_lower THEN 4
        WHEN LOWER(r.crag_name) LIKE :q_lower THEN 5
        WHEN LOWER(c.first_ascent) LIKE :q_lower THEN 6
        ELSE 7
    END
    """
    result = db.session.execute(text(sql), {"q_lower":"%"+q_lower+"%"})
    found_climbs = result.fetchall()
    return found_climbs

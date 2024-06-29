"""
This module defines the functions related to handling crags
for the Hyped app web application.
"""
import random
from sqlalchemy import text
from db import db


def get_all_crags():
    """Returns all crags and their info in alphabetical order"""
    sql = """
    SELECT id, crag_name, latitude, longitude, crag_description, manager, created_by
    FROM crags
    ORDER BY crag_name"""
    result = db.session.execute(text(sql))
    all_crags = result.fetchall()
    return all_crags


def get_crag(crag_id):
    """Returns information of a crag by the crag's id"""
    sql = """
    SELECT id, crag_name, latitude, longitude, crag_description, manager, created_by
    FROM crags
    WHERE id = :crag_id"""
    result = db.session.execute(text(sql), {"crag_id":crag_id})
    crag_info = result.fetchone()
    return crag_info


def max_min_grade_at_crag(crag_id):
    """Returns the highest and lowest grades (for climbs) at the crag"""
    sql = """
    SELECT MAX(s.difficulty) AS max_grade, MIN (s.difficulty) AS min_grade
    FROM crags c, climbs s
    WHERE c.id = s.crag_id
    AND c.id = :crag_id"""
    result = db.session.execute(text(sql), {"crag_id":crag_id})
    max_min = result.fetchone()
    return max_min


def get_random_crag():
    """Returns a valid crag id from the database so that a random crag can be retrieved"""
    sql = "SELECT id FROM crags"
    result = db.session.execute(text(sql))
    all_ids = [row[0] for row in result.fetchall()]
    return random.choice(all_ids)


def add_new_crag(name, latitude, longitude, description, manager, created_by):
    """Inserts a new crag into the database and returns its id"""
    try:
        sql = """
        INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by)
        VALUES (:name, :latitude, :longitude, :description, :manager, :created_by)
        RETURNING id"""
        result = db.session.execute(text(sql), {
            "name":name,
            "latitude":latitude,
            "longitude":longitude,
            "description":description,
            "manager":manager,
            "created_by":created_by
        })
        new_crag_id = result.fetchone()[0]
        db.session.commit()
    except Exception as e:
        print(e)
        return None
    return new_crag_id


def edit_crag(crag_id, crag_name, latitude, longitude, crag_description, manager):
    try:
        sql = """
        UPDATE crags
        SET crag_name = :crag_name,
            latitude = :latitude,
            longitude = :longitude,
            crag_description = :crag_description,
            manager = :manager
        WHERE id = :crag_id"""
        db.session.execute(text(sql), {
            "crag_name":crag_name,
            "latitude":latitude,
            "longitude":longitude,
            "crag_description":crag_description,
            "manager":manager,
            "crag_id":crag_id
        })
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True


def search_crags(query):
    """A search that shows more relevant results first"""
    q = query.lower()
    sql = """
    SELECT id, crag_name, latitude, longitude, crag_description, manager, created_by
    FROM crags 
    WHERE (
    LOWER(crag_name) LIKE :q 
    OR LOWER(crag_description) LIKE :q
    OR LOWER(manager) LIKE :q
    )
    ORDER BY
    CASE
        WHEN LOWER(crag_name) LIKE :q THEN 1
        WHEN LOWER(crag_description) LIKE :q THEN 2
        ELSE 3
    END"""
    result = db.session.execute(text(sql), {"q":"%"+q+"%"})
    found_crags = result.fetchall()
    return found_crags

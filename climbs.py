from db import db
from sqlalchemy import text


def get_all_climbs():
    sql = "SELECT * FROM climbs ORDER BY climb_name"
    result = db.session.execute(text(sql))
    all_climbs = result.fetchall()
    return all_climbs


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
from db import db
from sqlalchemy import text


def get_all_crags():
    sql = "SELECT id, crag_name, latitude, longitude, crag_description, manager, created_by FROM crags ORDER BY crag_name"
    result = db.session.execute(text(sql))
    all_crags = result.fetchall()
    return all_crags


def get_crag(id):
    sql = "SELECT id, crag_name, latitude, longitude, crag_description, manager, created_by FROM crags WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    crag_info = result.fetchone()
    return crag_info


def get_favourites(user_id):
    sql = """
    SELECT c.id, c.crag_name, c.latitude, c.longitude, c.crag_description, c.manager
    FROM crags c , favourite_crags f
    WHERE f.crag_id=c.id
    AND f.user_id=:user_id
    ORDER BY c.crag_name"""
    reusult = db.session.execute(text(sql), {"user_id":user_id})
    favourites = reusult.fetchall()
    return favourites


def add_new_crag(name, latitude, longitude, description, manager, created_by): 
    sql = """
    INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by)
    VALUES (:name, :latitude, :longitude, :description, :manager, :created_by)"""
    db.session.execute(text(sql), {"name":name, "latitude":latitude, "longitude":longitude, "description":description, "manager":manager, "created_by":created_by})
    db.session.commit()
    return True


def add_crag_to_favourites(user_id, crag_id): # not finished/tested
    sql = """
    INSERT INTO favourite_crags (user_id, crag_id)
    VALUES (:user_id, :crag_id)"""
    db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})


def search_crags(query): # search shows more relevant results first
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
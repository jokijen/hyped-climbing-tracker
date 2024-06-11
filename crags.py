from db import db
from sqlalchemy import text


def get_all_crags():
    sql = "SELECT * FROM crags ORDER BY crag_name"
    result = db.session.execute(text(sql))
    all_crags = result.fetchall()
    return all_crags


def get_crag(id):
    sql = "SELECT * FROM crags WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    crag_info = result.fetchone()
    return crag_info


def add_new_crag(name, latitude, longitude, description, created_by): 
    sql = """
    INSERT INTO crags (crag_name, latitude, longitude, crag_description, created_by)
    VALUES (:name, :latitude, :longitude, :description, :created_by)"""
    db.session.execute(text(sql), {"name":name, "latitude":latitude, "longitude":longitude, "description":description, "created_by":created_by})
    db.session.commit()
    return True


def add_crag_to_favourites(user_id, crag_id): # not finished/tested
    sql = """
    INSERT INTO favourite_crags (user_id, crag_id)
    VALUES (:user_id, :crag_id)"""
    db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})


def search_crags(query): 
    q = query.lower()
    sql = """
    SELECT * FROM crags 
    WHERE LOWER(crag_name) LIKE :q 
    OR LOWER(crag_description) LIKE :q
    OR LOWER(created_by) LIKE :q"""
    result = db.session.execute(text(sql), {"q":"%"+q+"%"})
    found_crags = result.fetchall()
    return found_crags
from db import db
from sqlalchemy import text
import random


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


def get_random_crag():
    sql = "SELECT id FROM crags"
    result = db.session.execute(text(sql))
    all_ids = [row[0] for row in result.fetchall()]    
    return random.choice(all_ids)


def add_new_crag(name, latitude, longitude, description, manager, created_by): 
    try:
        sql = """
        INSERT INTO crags (crag_name, latitude, longitude, crag_description, manager, created_by)
        VALUES (:name, :latitude, :longitude, :description, :manager, :created_by)"""
        db.session.execute(text(sql), {"name":name, "latitude":latitude, "longitude":longitude, "description":description, "manager":manager, "created_by":created_by})
        db.session.commit()
    except: 
        return False
    return True


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
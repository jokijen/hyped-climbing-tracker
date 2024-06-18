from db import db
from sqlalchemy import text


def get_favourites(user_id): # Returns all crags favourited by the user
    sql = """
    SELECT c.id, c.crag_name, c.latitude, c.longitude, c.crag_description, c.manager
    FROM crags c , favourite_crags f
    WHERE f.crag_id=c.id
    AND f.user_id=:user_id
    ORDER BY c.crag_name"""
    reusult = db.session.execute(text(sql), {"user_id":user_id})
    favourites = reusult.fetchall()
    return favourites


def is_in_favourites(user_id, crag_id): # Check if crag is already in favourite_crags of the user
    sql = """
    SELECT EXISTS (
    SELECT 1
    FROM favourite_crags 
    WHERE user_id=:user_id
    AND crag_id=:crag_id
    )"""
    result = db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})
    exists = result.fetchone()[0]
    return exists


def add_crag_to_favourites(user_id, crag_id): # Adds a crag to the user's favourite_crags
    try:
        sql = """
        INSERT INTO favourite_crags (user_id, crag_id)
        VALUES (:user_id, :crag_id)"""
        db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})
        db.session.commit()
    except: 
        return False
    return True
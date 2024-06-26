from db import db
from sqlalchemy import text


def get_favourites(user_id): # Returns all crags favourited by the user
    sql = """
    SELECT c.id, c.crag_name, c.latitude, c.longitude, c.crag_description, c.manager
    FROM crags c , favourite_crags f
    WHERE f.crag_id=c.id
    AND f.user_id=:user_id
    AND deleted IS NOT TRUE
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
    AND deleted IS NOT TRUE
    )"""
    result = db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})
    exists = result.fetchone()[0]
    return exists


def add_crag_to_favourites(user_id, crag_id): # Adds a crag to the user's favourite_crags (if already there but deleted, changes deleted = FALSE)
    try:
        sql = """
        INSERT INTO favourite_crags (user_id, crag_id)
        VALUES (:user_id, :crag_id)
        ON CONFLICT (user_id, crag_id) DO UPDATE
        SET DELETED = FALSE"""
        db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})
        db.session.commit()
    except: 
        return False
    return True


def delete_from_favourites(user_id, crag_id): # Delete favourite crag by marking it deleted
    try:
        sql = "UPDATE favourite_crags SET deleted = TRUE WHERE user_id=:user_id AND crag_id=:crag_id" 
        db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})
        db.session.commit()
    except: 
        return False
    return True


def times_favourited(crag_id): 
    sql = "SELECT COUNT(*) FROM favourite_crags WHERE crag_id=:crag_id"
    result = db.session.execute(text(sql), {"crag_id":crag_id})
    fav_count = result.fetchone()
    return fav_count[0]
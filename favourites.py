from db import db
from sqlalchemy import text


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


def add_crag_to_favourites(user_id, crag_id): # not finished/tested
    try:
        sql = """
        INSERT INTO favourite_crags (user_id, crag_id)
        VALUES (:user_id, :crag_id)"""
        db.session.execute(text(sql), {"user_id":user_id, "crag_id":crag_id})
        db.session.commit()
    except: 
        return False
    return True
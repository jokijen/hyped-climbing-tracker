from db import db
from sqlalchemy import text


def get_all_crags():
    sql = "SELECT * FROM crags"
    result = db.session.execute(text(sql))
    all_crags = result.fetchall()
    return all_crags

"""
def count_climbs():
    sql = "SELECT COUNT(*) FROM routes r, crags c WHERE r.crag_id = c.id"
    result = db.session.execute(text(sql))
    counter = result.fetchone()[0]
    return counter
    """

def add_crag(name, latitude, longitude, description, created_by):
    sql = """INSERT INTO crags (crag_name, latitude, longitude, crag_description, created_by)
    VALUES (:name, :latitude, :longitude, :description, :created_by)"""
    db.session.execute(text(sql), {"name":name, "latitude":latitude, "longitude":longitude, "description":description, "created_by":created_by})
    db.session.commit()
    return True
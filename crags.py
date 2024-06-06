from db import db
from sqlalchemy import text


def count_routes():
    sql = "SELECT COUNT(*) FROM routes r, crags c WHERE r.crag_id = c.id"
    result = db.session.execute(text(sql))
    counter = result.fetchone()[0]
    return counter

def add_crag():
    pass
from db import db


def count_routes():
    result = db.session.execute("SELECT COUNT(*) FROM routes r, crags c WHERE r.crag_id = c.id")
    counter = result.fetchone()[0]
    return counter

def add_crag():
    pass
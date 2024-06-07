from db import db
from sqlalchemy import text


def get_all_climbs():
    sql = "SELECT * FROM climbs"
    result = db.session.execute(text(sql))
    all_climbs = result.fetchall()
    return all_climbs
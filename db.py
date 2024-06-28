"""
This module sets up and configures the connection to the PostgreSQL 
database using SQLAlchemy
"""
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from sqlalchemy import Column, Integer, String, Table

from db import metadata

db_user = Table(
    "insta_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(120), unique=True, nullable=False),
    Column("email", String(120), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
)

import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text

from db import metadata

db_comment = Table(
    "insta_comment",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", Text, nullable=False),
    Column("username", String(120), nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=sqlalchemy.func.now()),
    Column(
        "post_id", ForeignKey("insta_post.id", ondelete="CASCADE"), nullable=False
    ),
)

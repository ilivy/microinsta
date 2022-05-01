# Import all the models, so that Base has them before being imported by Alembic

from app.db.base_class import Base
from app.db.tables.comments import Comment
from app.db.tables.posts import Post
from app.db.tables.users import User

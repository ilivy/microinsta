import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f"postgresql+asyncpg://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# if TESTING:
#     database = Database(TEST_DATABASE_URL, force_rollback=True)
# else:
#     database = Database(DATABASE_URL)

import aioredis, databases, sqlalchemy
import uuid, os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tutorbot")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

redis = aioredis.create_connection(address="redis://localhost")
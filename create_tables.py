from sqlalchemy import create_engine
from models import Base
from config import DATABASE_URL  # Import from the config file

def create_all_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, YourModel  # Import your models here

DATABASE_URL = "sqlite:///app.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    db = SessionLocal()
    try:
        # Add initial data to the database
        initial_data = [
            YourModel(field1='value1', field2='value2'),  # Replace with your model fields
            YourModel(field1='value3', field2='value4'),
        ]
        db.add_all(initial_data)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
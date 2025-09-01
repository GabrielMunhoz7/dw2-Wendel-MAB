from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Coin
from models import User

DATABASE_URL = "sqlite:///coins.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def seed_db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    db = SessionLocal()
    try:
        # Check if there's already data
        if db.query(Coin).count() > 0:
            print("Database already seeded")
            return

        # Add initial coin data. Image paths point to frontend assets.
        sample = [
            Coin(
                name="Denário Romano",
                period="Antigo",
                region="Roma",
                material="Prata",
                denomination="Denário",
                year="-200",
                description="Denário da República Romana.",
                image_front="assets/denario_front.jpg",
                image_back="assets/denario_back.jpg",
            ),
            Coin(
                name="Moeda Portuguesa",
                period="Moderno",
                region="Portugal",
                material="Cobre",
                denomination="Centavo",
                year="1910",
                description="Centavo do início do século XX.",
                image_front="assets/portugal_front.jpg",
                image_back="assets/portugal_back.jpg",
            ),
        ]

        db.add_all(sample)
        db.commit()
        print("Database seeded with sample coins")

        # create default admin user if not exists
        if db.query(User).filter(User.username == 'admin').count() == 0:
            admin = User(username='admin')
            admin.set_password('admin')
            db.add(admin)
            db.commit()
            print("Created default admin user (username: admin, password: admin) - change immediately")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
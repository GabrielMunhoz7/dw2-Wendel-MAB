from sqlalchemy import Column, Integer, String
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash


class Coin(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    period = Column(String, index=True, nullable=True)
    region = Column(String, index=True, nullable=True)
    material = Column(String, nullable=True)
    denomination = Column(String, nullable=True)
    year = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image_front = Column(String, nullable=True)
    image_back = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<Coin(id={self.id}, name={self.name}, period={self.period}, "
            f"region={self.region}, material={self.material})>"
        )

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True, index=True, nullable=False)
        password_hash = Column(String, nullable=False)

        def set_password(self, password: str):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password: str) -> bool:
            return check_password_hash(self.password_hash, password)
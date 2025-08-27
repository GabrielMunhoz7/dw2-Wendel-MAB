from sqlalchemy import Column, Integer, String
from database import Base

class ExampleModel(Base):
    __tablename__ = 'example_model'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    def __repr__(self):
        return f"<ExampleModel(id={self.id}, name={self.name}, description={self.description})>"
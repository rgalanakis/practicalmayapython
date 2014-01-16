from sqlalchemy import Column, Integer, String
# ... code to create the Base subclass
class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sound = Column(String)
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import relationship

engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", uselist=false, backref="user")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    item = relationship("Item", uselist=False, backref="owner")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
           
Base.metadata.create_all(engine)  #creates the tables in the database

sneezy = User(username="Sneezy", password="1234")
doc = User(username="Doc", password="5678")
grumpy = User("Grumpy", password="3456")

baseball = Item(name="Magic Baseball", description="You will always be a winner!", user_id=3)

session.add_all([])
session.commit()






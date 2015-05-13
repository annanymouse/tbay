#an item can only have one owner/user (one to one)
#a user can bid on many items and own many items (one to many)
#one item can have many bids (one to many)

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String, Date, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select

engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def divider(title):
    print("*"*30)
    print("{}".format(title))
    print("*"*30)
    
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    auctionable = relationship("Bid", backref="auction_item")
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    item = relationship("Item", backref="owner")
    bid = relationship("Bid", backref="bidder")
    
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
           
Base.metadata.create_all(engine)  #creates the tables in the database

sneezy = User(username="Sneezy", password="1234")
doc = User(username="Doc", password="5678")
grumpy = User(username="Grumpy", password="3456")

baseball = Item(name="Magic Baseball", description="You will always be a winner!", owner=grumpy)

bid1 = Bid(price=300.00, auction_item=baseball, bidder=sneezy)
bid2 = Bid(price=350.00, auction_item=baseball, bidder=doc)
bid3 = Bid(price=380.00, auction_item=baseball, bidder=sneezy)
bid4 = Bid(price=425.00, auction_item=baseball, bidder=doc)

session.add_all([sneezy, doc, grumpy, baseball, bid1, bid2, bid3, bid4])
session.commit()

divider("USERS")
for user in session.query(User).all():
    print("({}) {}, {}".format(user.id, user.username, user.password))

divider("AUCTION")
print("Item: {}\nDescription: {}\nOffered up for Auction by Owner:  {}\nAuction Start Time: {}"
      .format(baseball.name, baseball.description, baseball.owner.username, baseball.start_time))

divider("BIDS")
for bid in session.query(Bid).order_by(Bid.price):
    print("({}) {} bids {} on {}.".format(bid.id, bid.bidder.username, bid.price, bid.auction_item.name))
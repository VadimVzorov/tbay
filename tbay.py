#FIXME: Do i have to install sqlalchemy for every new project?
#It doesn't work before i install it in tbay folder.

#Answer: Install virtual environment for every new project
#FIXME:  python3 -m venv env --> to create virtual env
# to launch virtual env source env/bin/activate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://vadimvzorov:thinkful@localhost:5432/tbay')
#FIXME: How to create my own database?
Session = sessionmaker(bind=engine)
#FIXME: what is bind? -- use the connection
session = Session()
#FIXME: is this a temporaly
Base = declarative_base()
#FIXME: repository for the models, and will issue the
#create table statements to build up the database's table
#structure.

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

#user --> item owner 1:many
#user ---> bid item


class User(Base):
    __tablename__ = "users"
    id = Column (Integer, primary_key=True)
    username = Column (String, nullable=False)
    password = Column (String, nullable=False)
    my_items = relationship("Item", secondary="owner_association", backref="owner")
    # my_items_for_bids = relationship("Item", secondary="bid_association", backref="bidder")
    my_bids = relationship("Bid", uselist=False, backref="bids")

class Item(Base):
#FIXME: What is Base?
    __tablename__ = "items"
    # a string __tablename__, which will be used
    #to name the items table in the database.
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)

class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    bid_owner = Column(Integer, ForeignKey("users.id"), nullable=True)


owner_item_table = Table("owner_association", Base.metadata,
    Column("user", Integer, ForeignKey("users.id")),
    Column("item", Integer, ForeignKey("items.id"))
)

# bid_item_table = Table("bid_association", Base.metadata,
#     Column("user", Integer, ForeignKey("users.id")),
#     Column("item", Integer, ForeignKey("items.id"))
# )



Base.metadata.create_all(engine)

# import pdb; pdb.set_trace()

vadim = User(username="Vadim", password="12345")
emily = User(username="Emily", password="56789")
nastya = User(username="Nastya", password="09876")

ball = Item(name="Ball", description="red ball")
pen = Item(name="Pen", description="device for writing")
computer = Item(name="Computer", description="computer machine")

# bid1 = Bid(123)
# vadim.my_bids=bid1
nastya.my_items = [ball, pen, computer]
# vadim.my_items_for_bids = [ball, computer]
# vadim.my_bids=[]
# emily.my_items_for_bids = [pen, computer]
# emily.my_bids=[]

session.add_all([vadim, emily, nastya, ball, pen, computer])
session.commit()

bid1 = Bid(123, bid_owner=vadim)
session.add(bid1)
session.commit()

for x in vadim.my_items:
    print(x.name)
print(ball.owner[0].username)

print(vadim.bids)
# print(computer.bidder)

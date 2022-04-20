from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from datetime import datetime
"""
Alembic Commands:
    alembic revision --autogenerate -m "initial migration"
    alembic upgrade head
"""

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_banned = Column(Boolean, nullable=False, default=False)
    address = Column(String, nullable=False)
    first_name  = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username={self.username}, password={self.password}, is_admin={self.is_admin}, is_banned={self.is_banned}, address={self.address}, first_name={self.first_name}, last_name={self.last_name}, city={self.city}, email={self.email})>"

class Notification(Base):
    __tablename__ = 'notification'
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    notif_desc = Column(String, nullable=False)
    date_made = Column(DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"<Notification(notification_id={self.notification_id}, user_id={self.user_id}, notif_desc={self.notif_desc}, date_made={self.date_made})"

class Item(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    warning_id = Column(Integer, ForeignKey('warning.warning_id'), nullable=False)
    item_name = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    item_desc = Column(String, nullable=False)
    pic_url = Column(String, nullable=False)
    is_biddable = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Item(item_id={self.item_id}, user_id={self.user_id}, warning_id={self.warning_id}, price={self.price}, item_desc={self.item_desc}, pic_url={self.pic_url}, is_biddable={self.is_biddable})"

class Warnings(Base):
    __tablename__ = 'warning'
    warning_id = Column(Integer, primary_key=True)
    warning_desc = Column(String, nullable=False)

    def __repr__(self):
        return f"<Warning(warning_id={self.warning_id}, warning_desc={self.warning_desc})"

class Bidding(Base):
    __tablename__ = 'bidding'
    bid_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    top_bid = Column(Float, nullable=False)
    bid_expire_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Bidding(bid_id={self.bid_id}, item_id={self.item_id}, user_id={self.user_id}, top_bid={self.top_bid}, bid_expire_date={self.bid_expire_date})"

class Orders(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    bid_id = Column(Integer, ForeignKey('bidding.bid_id'), nullable=False)

    def __repr__(self):
        return f"<Orders(order_id={self.order_id}, item_id={self.item_id}, user_id={self.user_id}, bid_id={self.bid_id})"

class Reviews(Base):
    __tablename__ = 'review'
    review_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    message = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Reviews(review_id={self.review_id}, item_id={self.item_id}, user_id={self.user_id}, message={self.message}, rating={self.rating})"
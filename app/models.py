from app import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Float, Enum
from enum import Enum as UserEnum


# Tat ca cac model deu phai ke thua db.Model
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Categories(BaseModel):
    category_name = Column(String(50), nullable=False)
    books = relationship('Books', backref='Categories', lazy=True)


class Books(BaseModel):
    book_name = Column(String(150), nullable=False)
    author_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    import_date = Column(DateTime, nullable=False)
    unit_price = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    order_details = relationship('OrderDetails', backref='Books', lazy=True)


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class UserAccount(BaseModel):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(250), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    orders = relationship('Orders', backref='UserAccount', lazy=True)


class Orders(BaseModel):
    order_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey(UserAccount.id), nullable=False)
    order_details = relationship('OrderDetails', backref='Orders', lazy=True)


class OrderDetails(BaseModel):
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0)
    order_id = Column(Integer, ForeignKey(Orders.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Books.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

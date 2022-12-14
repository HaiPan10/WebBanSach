import hashlib
from datetime import datetime

from app import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Float, Enum, Text, Boolean
from enum import Enum as UserEnum, Enum as StatusEnum
from flask_login import UserMixin


# Tat ca cac model deu phai ke thua db.Model
class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Categories(BaseModel):
    category_name = Column(String(50), nullable=False)
    books = relationship('Books', backref='categories', lazy=True)
    descriptions = Column(Text)
    image = Column(String(250))

    def __str__(self):
        return self.category_name


class Books(BaseModel):
    book_name = Column(String(150), nullable=False)
    author_name = Column(String(100))
    quantity = Column(Integer, default=0)
    import_date = Column(DateTime)
    unit_price = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    order_details = relationship('OrderDetails', backref='books', lazy=True)
    sold_numbers = Column(Integer, default=0)
    image = Column(String(250), nullable=False)
    descriptions = Column(Text)
    comments = relationship('Comment', backref='books', lazy=True)

    def __str__(self):
        return self.book_name


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class Status(StatusEnum):
    DA_THANH_TOAN = 1
    DANG_GIAO = 2
    CHUA_THANH_TOAN = 3

    def __str__(self):
        if self is Status.DA_THANH_TOAN:
            return "Đã thanh toán"
        elif self is Status.DANG_GIAO:
            return "Đang giao"
        else:
            return "Chưa thanh toán"


class UserAccount(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(250), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    phone_number = Column(String(10), nullable=True, unique=True)
    orders = relationship('Orders', backref='user_account', lazy=True)
    comments = relationship('Comment', backref='user_account', lazy=True)

    def __str__(self):
        return self.name


class Orders(BaseModel):
    order_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey(UserAccount.id), nullable=False)
    order_details = relationship('OrderDetails', backref='orders', lazy=True)
    address = Column(String(250), nullable=True)
    status = Column(Enum(Status), default=Status.CHUA_THANH_TOAN)


class OrderDetails(BaseModel):
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0)
    order_id = Column(Integer, ForeignKey(Orders.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Books.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_account_id = Column(Integer, ForeignKey(UserAccount.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Books.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        pass
        # db.drop_all()
        # db.create_all()
        # name = 'Admin'
        # username = 'admin'
        # password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # avatar = 'https://res.cloudinary.com/dxjkpbzmo/image/upload/v1669562707/user_admin-removebg-preview_xtqp2h.png'
        # user = UserAccount(name=name, username=username, password=password, avatar=avatar, user_role=UserRole.ADMIN)
        # db.session.add(user)
        # db.session.commit()
        # db.drop_all()

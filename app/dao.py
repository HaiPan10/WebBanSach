from sqlalchemy import func

from app.models import UserAccount, Books, Categories, Orders, OrderDetails, UserRole, UserAccount
from app import db
import hashlib


def load_books(cate_id=None, keyword=None, from_price=None, to_price=None, is_available=None):
    query = Books.query
    if cate_id:
        query = query.filter(Books.category_id.__eq__(cate_id))

    if keyword:
        # query danh muc va ten sach tuong ung keyword
        query_book_name = query.filter(Books.book_name.contains(keyword))

        # query danh muc va ten tac gia tuong ung keyword
        query_author_name = query.filter(Books.author_name.contains(keyword))
        query = query_book_name.union(query_author_name)

    if from_price:
        query = query.filter(Books.unit_price.__ge__(from_price))

    if to_price:
        query = query.filter(Books.unit_price.__le__(to_price))

    if is_available:
        query = query.filter(Books.quantity.__ge__(1))
        if from_price:
            query = query.filter(Books.unit_price.__ge__(from_price))

        if to_price:
            query = query.filter(Books.unit_price.__le__(to_price))
    return query.all()


def get_book_by_id(book_id):
    return Books.query.get(book_id)


def get_max_price():
    return db.session.query(func.max(Books.unit_price)).scalar()


def get_quantity_by_id(book_id):
    return db.session.query(Books).filter(Books.id.__eq__(book_id)).first().quantity


def get_min_price():
    return db.session.query(func.min(Books.unit_price)).scalar()


def load_categories():
    return Categories.query.all()


def load_order_by_id(order_id):
    return Orders.query.get(order_id)


def load_orders():
    return Orders.query.all()


def create_account(name, username, password, avatar):
    pw = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = UserAccount(name=name, username=username, password=pw, avatar=avatar)


def auth_user(username, password):
    # Ma hoa password su dung ham bang
    pw = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return UserAccount.query.filter(UserAccount.username.__eq__(username),
                                    UserAccount.password.__eq__(pw)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = UserAccount(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_category_name(category_id):
    return Categories.query.get(category_id).category_name


def get_user_by_id(user_id):
    return UserAccount.query.get(user_id)

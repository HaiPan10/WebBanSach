from app.models import UserAccount, Books, Categories, Orders, OrderDetails, UserRole, UserAccount
from app import db
import hashlib


def load_books(cate_id=None, keyword=None):
    query = Books.query
    if cate_id:
        query = query.filter(Books.category_id.__eq__(cate_id))

    if keyword:
        query = query.filter(Books.book_name.contains(keyword))

    return query.all()


def get_book_by_id(book_id):
    return Books.query.get(book_id)


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

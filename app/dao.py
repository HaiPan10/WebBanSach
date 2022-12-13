import datetime

from flask_login import current_user
from sqlalchemy import func, update, and_, cast, Integer, extract

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


def select_top_best_seller(top_num):
    return db.session.query(Books.id, Books.book_name, Books.unit_price, Books.image, Books.quantity,
                            func.max(Books.sold_numbers)) \
        .group_by(Books.id).order_by(Books.sold_numbers.desc()).limit(top_num).all()


def select_top_category(top_num):
    return db.session.query(Categories.id, Categories.category_name, Categories.image, func.max(Books.sold_numbers)) \
        .join(Books, Books.category_id.__eq__(Categories.id), isouter=True) \
        .group_by(Categories.id).order_by(Books.sold_numbers.desc()).limit(top_num).all()


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


def register(name, username, phone, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = UserAccount(name=name, username=username, phone_number=phone, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_category_name(book_id):
    return Categories.query.filter(and_(Books.category_id.__eq__(Categories.id), Books.id.__eq__(book_id))).first()


def get_user_by_id(user_id):
    return UserAccount.query.get(user_id)


def save_receipt(cart, address, status):
    if cart:
        order = Orders(UserAccount=current_user, order_date=datetime.datetime.now(),
                       address=address, status=status)
        db.session.add(order)
        for c in cart.values():
            d = OrderDetails(quantity=c['quantity'], unit_price=c['unit_price'],
                             Orders=order, book_id=c['id'])
            db.session.add(d)
        db.session.commit()
        # Trả về order id vừa mới tạo
        return order.id


def get_max_order_id():
    return Orders.query(func.max(Orders.id)).scalar()


def load_book_by_order_id(order_id):
    return db.session.query(Books.id, Books.book_name, OrderDetails.quantity,
                            OrderDetails.unit_price, OrderDetails.id) \
        .join(OrderDetails, Books.id.__eq__(OrderDetails.book_id)) \
        .where(OrderDetails.order_id.__eq__(order_id)) \
        .all()


def stats_revenue():
    total_revenue = db.session.query(func.sum(OrderDetails.unit_price * OrderDetails.quantity)).scalar()

    query = db.session.query(Categories.id, Categories.category_name,
                             func.sum(OrderDetails.unit_price * OrderDetails.quantity), func.count(Books.id),
                             (100 * func.sum(OrderDetails.unit_price * OrderDetails.quantity) / total_revenue))\
        .join(Books, Books.category_id.__eq__(Categories.id))\
        .join(OrderDetails, OrderDetails.book_id.__eq__(Books.id))\
        .join(Orders, OrderDetails.order_id.__eq__(Orders.id)).filter(extract('month', Orders.order_date) == 11)

    return query.group_by(Categories.id).order_by(-Categories.id).all()

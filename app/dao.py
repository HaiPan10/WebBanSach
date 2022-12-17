from datetime import datetime, timedelta

from flask_login import current_user
from sqlalchemy import func, update, and_, cast, Integer, extract, event, DDL
from sqlalchemy.exc import DataError

from app.models import UserAccount, Books, Categories, Orders, OrderDetails, UserRole, UserAccount, Comment, Status
from app import db, utils, app
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
        order = Orders(user_account=current_user, order_date=datetime.now(),
                       address=address, status=Status(status))
        db.session.add(order)
        for c in cart.values():
            book = Books.query.where(Books.id.__eq__(c['id'])).first()
            if book.quantity >= c['quantity']:
                d = OrderDetails(quantity=c['quantity'], unit_price=c['unit_price'],
                                 orders=order, book_id=c['id'])
                book.quantity -= c['quantity']
                book.sold_numbers += c['quantity']
            else:
                raise ValueError("{} số lượng tồn không đủ".format(book.book_name))
            db.session.add(d)
        db.session.commit()
        # Trả về order id vừa mới tạo
        return True


def get_max_order_id():
    return Orders.query(func.max(Orders.id)).scalar()


def load_book_by_order_id(order_id):
    return db.session.query(Books.id, Books.book_name, OrderDetails.quantity,
                            OrderDetails.unit_price, OrderDetails.id) \
        .join(OrderDetails, Books.id.__eq__(OrderDetails.book_id)) \
        .where(OrderDetails.order_id.__eq__(order_id)) \
        .all()


def check_user_name(username):
    user = UserAccount.query.where(UserAccount.username.__eq__(username)).first()
    return True if user else False


def check_phone_number(phone_number):
    user = UserAccount.query.where(UserAccount.phone_number.__eq__(phone_number)).first()
    return True if user else False


def stats_revenue(month, year):
    total_revenue = db.session.query(func.sum(OrderDetails.unit_price * OrderDetails.quantity)) \
        .join(Orders, OrderDetails.order_id.__eq__(Orders.id)) \
        .filter(extract('month', Orders.order_date) == month, extract('year', Orders.order_date) == year,
                Orders.status.__eq__(True))

    query = db.session.query(Categories.id, Categories.category_name,
                             func.sum(OrderDetails.unit_price * OrderDetails.quantity), func.count(Books.id),
                             (100 * func.sum(OrderDetails.unit_price * OrderDetails.quantity) / total_revenue)) \
        .join(Books, Books.category_id.__eq__(Categories.id)) \
        .join(OrderDetails, OrderDetails.book_id.__eq__(Books.id)) \
        .join(Orders, OrderDetails.order_id.__eq__(Orders.id)) \
        .filter(extract('month', Orders.order_date) == month, extract('year', Orders.order_date) == year,
                Orders.status.__eq__(True))

    return query.group_by(Categories.id).order_by(Categories.id).all()


def stats_frequency(month, year):
    total_frequency = db.session.query(func.sum(OrderDetails.quantity)) \
        .join(Orders, OrderDetails.order_id.__eq__(Orders.id)) \
        .filter(extract('month', Orders.order_date) == month, extract('year', Orders.order_date) == year,
                Orders.status.__eq__(True))

    query = db.session.query(Books.id, Books.book_name, Categories.category_name, func.sum(OrderDetails.quantity),
                             (100 * func.sum(OrderDetails.quantity)) / total_frequency) \
        .join(Categories, Categories.id.__eq__(Books.category_id)) \
        .join(OrderDetails, OrderDetails.book_id.__eq__(Books.id)) \
        .join(Orders, OrderDetails.order_id.__eq__(Orders.id)) \
        .filter(extract('month', Orders.order_date) == month, extract('year', Orders.order_date) == year,
                Orders.status.__eq__(True))
    return query.group_by(Books.id).order_by(Books.id).all()


def get_min_year():
    return db.session.query(func.min(extract('year', Orders.order_date))).scalar()


def load_comments(book_id):
    return Comment.query.filter(Comment.book_id.__eq__(book_id)).order_by(-Comment.id).all()


def save_comment(content, book_id):
    c = Comment(content=content, book_id=book_id, user_account=current_user)
    db.session.add(c)
    db.session.commit()

    return c


def get_orders(user_id):
    return db.session.query(Orders.id, Orders.address, Orders.order_date,
                            func.sum(OrderDetails.quantity * OrderDetails.unit_price).label('total_amount'),
                            Orders.status) \
        .where(Orders.user_id.__eq__(user_id)) \
        .join(OrderDetails, OrderDetails.order_id.__eq__(Orders.id)) \
        .group_by(Orders.id).all()


def get_order_details(order_id):
    return db.session.query(Books.id, Books.book_name, OrderDetails.quantity, OrderDetails.unit_price) \
        .where(OrderDetails.order_id.__eq__(order_id)) \
        .join(OrderDetails, OrderDetails.book_id.__eq__(Books.id)) \
        .order_by(Books.id).all()


def get_query_order_details(order_id):
    return OrderDetails.query.filter(OrderDetails.order_id.__eq__(order_id))


def delete_order_schedule():
    order = Orders.query.filter(Orders.status.__eq__(Status.CHUA_THANH_TOAN)).all()
    rules = utils.read_rules()
    for o in order:
        # print(o.order_date)
        # print(o.order_date + timedelta(days=int(rules['delete_time'])))
        # print(datetime.now())
        if o.status is Status.CHUA_THANH_TOAN and \
                (o.order_date + timedelta(days=int(rules['delete_time']))) <= datetime.now():
            order_details_query = get_query_order_details(o.id)
            order_details_query.delete()
            Orders.query.filter(Orders.id.__eq__(o.id)).delete()

    db.session.commit()


# @event.listens_for(Orders, 'after_insert')
# def after_commit(mapper, connection, target):
#     rules = utils.read_rules()
#     delete_order_event = DDL('''
#             CREATE EVENT delete_order_{0}_schedule
#             ON SCHEDULE AT CURRENT_TIMESTAMP() + INTERVAL '{1}' HOUR_MINUTE
#             DO
#                 CALL delete_order({0}, {2})
#             '''.format(target.id, rules['delete_time'], target.status.value))
#     connection.execute(delete_order_event)

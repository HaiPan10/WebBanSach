from app import dao, app

with app.app_context():
    print(dao.load_book_by_order_id(4))

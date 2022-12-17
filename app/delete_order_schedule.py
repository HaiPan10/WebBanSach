from app import dao, app

# hang ngay vao luc 0h00 he thong tu dong chay 1 file duy nhat
with app.app_context():
    dao.delete_order_schedule()

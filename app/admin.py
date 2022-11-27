from app.models import Categories, Books, Orders, OrderDetails
from app import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


# Kế thừa model view có sẵn
class BooksView(ModelView):
    column_searchable_list = ['book_name', 'id']
    column_labels = {
        'id': 'Mã sản phẩm',
        'book_name': 'Tên sản phẩm',
        'author_name': 'Tên tác giả',
        'unit_price': 'Đơn giá',
        'quantity': 'Số lượng',
        'import_date': 'Ngày nhập',
        'category_id': 'Mã thể loại'
    }

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


admin = Admin(app=app, name='Quản Trị Bán Sách', template_mode='bootstrap4')
admin.add_view(BooksView(Books, db.session, name='Các Sản Phẩm Sách'))

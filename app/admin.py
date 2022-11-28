import getpass

from flask_admin.contrib.sqla.fields import QuerySelectField

from app.models import Categories, Books, Orders, OrderDetails
from app import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin.form import rules, fields, form, Select2Widget
from wtforms import SelectField, StringField, FileField
import cloudinary.uploader


# Upload ảnh lên cloudinary
def upload_cloudinary(image):
    res = cloudinary.uploader.upload(image)
    image = res['secure_url']
    return image


# Kế thừa model view có sẵn
class BooksView(ModelView):
    column_list = ['id', 'book_name', 'author_name', 'unit_price',
                   'quantity', 'import_date', 'category_id']
    column_searchable_list = ['book_name', 'id']
    column_filters = ['book_name', 'unit_price']
    can_view_details = True
    column_exclude_list = ['image']
    column_labels = {
        'id': 'Mã sản phẩm',
        'book_name': 'Tên sản phẩm',
        'author_name': 'Tên tác giả',
        'unit_price': 'Đơn giá',
        'quantity': 'Số lượng',
        'import_date': 'Ngày nhập',
        'category_id': 'Mã thể loại'
    }

    with app.app_context():
        form_create_rules = ('book_name', 'author_name', 'unit_price', 'image', 'category_id', 'descriptions')
        form_edit_rules = ('book_name', 'author_name', 'unit_price', 'category_id', 'descriptions')
        form_extra_fields = {
            'category_id': QuerySelectField(
                label='Thể loại',
                query_factory=lambda: Categories.query.all(),
                widget=Select2Widget()),
            'image': FileField('Ảnh minh họa')
        }

    def on_model_change(self, form, model, is_created):
        # lay noi dung form cua nguoi dung
        if is_created:
            curr_user = getpass.getuser()
            model.updatedby = curr_user
            # chinh sua lai image thanh chuoi duong dan
            model.image = upload_cloudinary(form['image'].data)

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


class CategoriesView(ModelView):
    form_create_rules = ('category_name', 'image', 'descriptions')
    form_edit_rules = ('category_name', 'descriptions')
    form_extra_fields = {
        'image': FileField('Ảnh minh họa')
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            # lay noi dung form cua nguoi dung
            curr_user = getpass.getuser()
            model.updatedby = curr_user
            # chinh sua lai image thanh chuoi duong dan
            model.image = upload_cloudinary(form['image'].data)

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


class InputBooksView(ModelView):
    form_create_rules = ('import_date', 'quantity')
    can_create = False
    can_delete = False

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


admin = Admin(app=app, name='Quản Trị Bán Sách', template_mode='bootstrap4')
admin.add_view(BooksView(Books, db.session, name='Các Sản Phẩm Sách', endpoint='admin-input'))
admin.add_view(CategoriesView(Categories, db.session, name='Danh mục'))
admin.add_view(InputBooksView(Books, db.session, name='Nhập sách', endpoint='admin-input-quantity'))

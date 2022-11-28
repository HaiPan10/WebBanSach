import datetime
from flask import flash, redirect
from flask_admin.babel import gettext
from wtforms.validators import InputRequired, NumberRange

from app.models import Categories, Books, Orders, OrderDetails
from app import db, app, utils
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import SelectField, StringField, FileField, Form, DateField, IntegerField
import cloudinary.uploader


# Upload ảnh lên cloudinary
def upload_cloudinary(image):
    res = cloudinary.uploader.upload(image)
    image = res['secure_url']
    return image


# class InputQuantityForm(Form):
#     import_date = DateField('Ngày nhập kho', format="%d-%m-%Y")
#     import_quantity = IntegerField('Số lượng nhập')


# Kế thừa model view có sẵn
class BooksView(ModelView):
    column_formatters = dict(category_id=lambda v, c, m, p: Categories.query.get(m.category_id).category_name)
    column_list = ['id', 'book_name', 'author_name', 'unit_price',
                   'quantity', 'import_date', 'category_id']
    column_searchable_list = ['id', 'book_name']
    column_filters = ['book_name', 'unit_price']
    can_view_details = True
    column_exclude_list = ['image']
    column_labels = {
        'id': 'Mã sản phẩm',
        'book_name': 'Tên sản phẩm',
        'author_name': 'Tên tác giả',
        'unit_price': 'Đơn giá',
        'quantity': 'Số lượng',
        'import_date': 'Ngày nhập kho',
        'category_id': 'Tên thể loại'
    }

    with app.app_context():
        form_create_rules = ('book_name', 'author_name', 'unit_price', 'image', 'category_id', 'descriptions')
        form_edit_rules = ('book_name', 'author_name', 'unit_price', 'category_id', 'descriptions')
        form_extra_fields = {
            'category_id': SelectField('Loại sản phẩm', coerce=int,
                                       choices=lambda: [(c.id, c.category_name) for c in Categories.query.all()],
                                       validators=[InputRequired()]),
            'image': FileField('Ảnh minh họa', validators=[InputRequired()])
        }

    def on_model_change(self, form, model, is_created):
        # lay noi dung form cua nguoi dung
        if is_created:
            # chi khi nao tao moi moi upload anh len cloudinary
            # chinh sua lai image thanh chuoi duong dan
            model.image = upload_cloudinary(form['image'].data)

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


class CategoriesView(ModelView):
    form_create_rules = ('category_name', 'image', 'descriptions')
    form_edit_rules = ('category_name', 'descriptions')
    form_extra_fields = {
        'image': FileField('Ảnh minh họa', validators=[InputRequired()])
    }

    def on_model_change(self, form, model, is_created):
        if is_created:
            # lay noi dung form cua nguoi dung
            # chinh sua lai image thanh chuoi duong dan
            model.image = upload_cloudinary(form['image'].data)

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


class InputBooksView(ModelView):
    column_formatters = dict(category_id=lambda v, c, m, p: Categories.query.get(m.category_id).category_name)
    column_list = ['id', 'book_name', 'author_name', 'unit_price',
                   'quantity', 'import_date', 'category_id']
    column_labels = {
        'id': 'Mã sản phẩm',
        'book_name': 'Tên sản phẩm',
        'author_name': 'Tên tác giả',
        'unit_price': 'Đơn giá',
        'quantity': 'Số lượng',
        'import_date': 'Ngày nhập kho',
        'category_id': 'Tên thể loại'
    }
    # Mot doi tuong dict ve quy dinh nhap
    rules = utils.read_rules()

    form_edit_rules = ('quantity',)
    # validators ràng buộc cho cái input
    form_extra_fields = {
        'quantity': IntegerField('Số lượng nhập thêm vào kho', validators=[InputRequired()])
    }
    can_create = False
    can_delete = False

    def on_form_prefill(self, form, id):
        # Doc lai quy dinh them lan nua
        self.rules = utils.read_rules()
        form['quantity'].data = 0

    # Ràng buộc việc nhập số lượng ghi đè update_model
    def update_model(self, form, model):
        if form['quantity'].data < int(self.rules['quantity_import']):
            flash(gettext('Số lượng nhập dưới mức tối thiểu ' + self.rules['quantity_import']), 'error')
            return False
        else:
            # Dữ liệu nhập đúng cập nhật lên database
            model.quantity += form['quantity'].data
            model.import_date = datetime.datetime.now()
            db.session.add(model)
            db.session.commit()
            return True

    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


class AdjustView(BaseView):
    @expose('/')  # vào expose tham chiếu đến một trang custom mới
    def index(self):  # Ghi đè lên hàm index
        # Lấy thông tin về số lượng
        rules = utils.read_rules()
        return self.render('admin/adjust_rules.html', rules=rules)


admin = Admin(app=app, name='Quản Trị Bán Sách', template_mode='bootstrap4')
admin.add_view(BooksView(Books, db.session, name='Các Sản Phẩm Sách', endpoint='admin-input'))
admin.add_view(CategoriesView(Categories, db.session, name='Danh mục'))
admin.add_view(InputBooksView(Books, db.session, name='Nhập kho', endpoint='admin-input-quantity'))
admin.add_view(AdjustView(name='Thay đổi quy định'))

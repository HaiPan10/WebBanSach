from app.models import Categories
from app import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


# Kế thừa model view có sẵn
class BooksView(ModelView):
    def is_accessible(self):  # Xac thuc truy cap nguoi dung
        return current_user.is_authenticated


admin = Admin(app=app, name='Quản Trị Bán Sách')

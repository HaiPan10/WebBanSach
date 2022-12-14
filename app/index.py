# Định tuyến tới biến app trang init.py
import requests

from app.admin import InputBooksView
from app.models import UserRole
from app import app, dao, login, utils, admin as ad, controllers
# Import render_template để dùng render_template
from flask import render_template, redirect, session, jsonify, make_response
# Dùng request để đổ product theo cate_id
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app.decorator import annonymous_user
import cloudinary
import cloudinary.uploader


app.add_url_rule("/", 'index', controllers.home)
app.add_url_rule("/products", 'products', controllers.product_list)
app.add_url_rule("/products/product_id=<int:book_id>", 'product-details', controllers.product_detail)
app.add_url_rule("/login-admin", 'login-admin', controllers.admin_login, methods=['post'])
app.add_url_rule("/register", 'register', controllers.register, methods=['post', 'get'])
app.add_url_rule("/login", 'login-my-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule("/logout", 'logout-my-user', controllers.logout_my_user)
app.add_url_rule("/admin/adjustview/change", 'adjust-rules', controllers.adjust_rules, methods=['post'])
app.add_url_rule("/api/cart", 'add-to-cart', controllers.add_to_cart, methods=['post'])
app.add_url_rule("/api/delete_cart/<product_id>", 'delete-cart', controllers.delete_cart, methods=['delete'])
app.add_url_rule("/api/update_cart/<product_id>", 'update-cart', controllers.update_cart, methods=['put'])
app.add_url_rule("/api/pay", 'pay', controllers.pay, methods=['post'])
app.add_url_rule("/api/pay_with_momo", 'pay-with-momo', controllers.pay_with_momo, methods=['post'])
app.add_url_rule("/api/momo_result", 'momo-result', controllers.momo_result, methods=['get'])
app.add_url_rule("/cart_details", 'cart-details', controllers.cart_view)
app.add_url_rule("/checkout", 'checkout', controllers.checkout)


# login người dùng tại đây
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attr():
    return {
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']), message='')
    }


# Chạy trang web
if __name__ == '__main__':
    app.run(debug=True)
    # Cờ debug bật để kiểm tra lỗi, triển khai lên sever phải tắt đi

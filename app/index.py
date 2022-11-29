# Định tuyến tới biến app trang init.py
from app.admin import InputBooksView
from app.models import UserRole
from app import app, dao, login, utils, admin as ad
# Import render_template để dùng render_template
from flask import render_template, redirect
# Dùng request để đổ product theo cate_id
from flask import request
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
from app.decorator import annonymous_user


# Định nghĩa đường dẫn
@app.route("/")
def home():
    # Đổ dữ liệu category
    categories = dao.load_categories()

    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    products = dao.load_books(cate_id=cate_id)

    return render_template('index.html', categories=categories, count=0, products=products)


# Chuyển trang product
@app.route("/products")
def product_list():
    # Đổ dữ liệu theo cate_id
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    products = dao.load_books(cate_id=cate_id)
    categories = dao.load_categories()
    return render_template('products.html', products=products, categories=categories)


# Cấu hình trang chi tiết sản phẩm
@app.route("/products/<int:id>")
def product_detail(book_id):
    product = dao.get_book_by_id()
    return render_template('product_detail.html', product=product)


@app.route("/login-admin", methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    # nếu có tồn tại user khớp với username và password
    if user and user.user_role == UserRole.ADMIN:
        login_user(user=user)
    return redirect('/admin')


# login người dùng tại đây
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


# register người dùng
@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['repassword']
        if password.__eq__(confirm):
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password,
                             avatar=avatar)
                return redirect('/login')
            except:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau"
        else:
            err_msg = 'Mật khẩu không khớp'
    return render_template("register.html", err_msg=err_msg)


# login người dùng
@app.route("/login", methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect('/')
    return render_template('login.html')


# logout
@app.route('/logout')
@login_required
def logout_my_user():
    logout_user()
    return redirect('/')


@app.route("/admin/adjustview/change", methods=['post'])
def adjust_rules():
    quantity_import = request.form['quantity_import']
    quantity_in_stocks = request.form['quantity_in_stocks']
    rules = {
        'quantity_import': quantity_import,
        'quantity_in_stocks': quantity_in_stocks
    }
    utils.write_json('data/adjust_rules.json', file=rules)
    # Cập nhật lại thông tin của input books view
    for view in ad.admin.__getattribute__('_views'):
        if isinstance(view, InputBooksView):
            view.read_rules()
    return redirect("/admin")


# Chạy trang web
if __name__ == '__main__':
    app.run(debug=True)
    # Cờ debug bật để kiểm tra lỗi, triển khai lên sever phải tắt đi

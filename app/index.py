# Định tuyến tới biến app trang init.py
from app.admin import InputBooksView
from app.models import UserRole
from app import app, dao, login, utils, admin as ad
# Import render_template để dùng render_template
from flask import render_template, redirect, session, jsonify
# Dùng request để đổ product theo cate_id
from flask import request
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
from app.decorator import annonymous_user


# Định nghĩa đường dẫn
@app.route("/")
def home():
    # Đổ dữ liệu category
    error_message = None
    products = []
    categories = []
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    try:
        products = dao.load_books(cate_id=cate_id)
        categories = dao.load_categories()
    except:
        error_message = 'Hệ thống bảo trì'
    return render_template('index.html', categories=categories, count=0, products=products, error_message=error_message)


# Chuyển trang product
@app.route("/products")
def product_list():
    # số sản phẩm hiện trong 1 trang
    max_amount_per_page = 6

    # lấy loại sách được chọn
    cate_id = request.args.get("category_id")

    # load dữ liệu category
    categories = dao.load_categories()

    # lấy chuỗi tìm kiếm
    kw = request.args.get("keyword")

    # lấy tất cả sản phẩm đổ vào autocomplete
    all_products = list(dao.load_books())
    list_products_name = []
    for p in all_products:
        list_products_name.append(str(p.book_name))
        list_products_name.append(str(p.author_name))

    # Xử lý lọc theo giá
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    if from_price is None:
        from_price = dao.get_min_price()
    if to_price is None:
        to_price = dao.get_max_price()

    # Trang hiện tại
    page = request.args.get("page")
    if page is None:
        page = 1
    else:
        page = int(page)

    # Lấy dữ liệu sản phẩm
    products = list(dao.load_books(cate_id=cate_id, keyword=kw, from_price=from_price, to_price=to_price))

    # Xử lý sort
    sort_value = request.args.get('sort_choice')
    if sort_value is None:
        sort_value = 1
        products = sorted(products, key=lambda x: x.book_name, reverse=False)
    if int(sort_value) == 5:
        products = dao.load_books(cate_id=cate_id, from_price=from_price, to_price=to_price, is_available=True)
    if int(sort_value) == 4:
        products = sorted(products, key=lambda x: x.unit_price, reverse=True)
    elif int(sort_value) == 3:
        products = sorted(products, key=lambda x: x.unit_price, reverse=False)
    elif int(sort_value) == 2:
        products = sorted(products, key=lambda x: x.book_name, reverse=True)
    else:
        products = sorted(products, key=lambda x: x.book_name, reverse=False)

    # Tính số trang
    page_count = int(len(products) / max_amount_per_page)
    if len(products) % max_amount_per_page != 0:
        page_count = page_count + 1

    return render_template('products.html', products=products, categories=categories,
                           page_count=page_count, page=page, max_amount_per_page=max_amount_per_page,
                           cate_id=cate_id, list_products_name=list_products_name,
                           from_price=from_price, to_price=to_price,
                           min_price=dao.get_min_price(), max_price=dao.get_max_price(),
                           sort_value=sort_value, product_count = len(products))


# Cấu hình trang chi tiết sản phẩm
@app.route("/products/product_id=<int:book_id>", methods=['get', 'post'])
def product_detail(book_id):
    # format đường dẫn như sau:
    # /products/product_id={{products[i].id}}?category_id={{cate_id}}&i={{i}}
    # cate_id lấy từ view /products
    # Gia trị i là giá trị index theo thứ tự của list trong products
    i = int(request.args.get("i"))
    cate_id = request.args.get("category_id")
    products = dao.load_books(cate_id=cate_id) if not cate_id.__eq__('None') else dao.load_books()
    product = dao.get_book_by_id(book_id)
    category_name = dao.get_category_name(products[i].category_id)
    size = len(products) - 1
    curr = None
    if request.method.__eq__('POST'):
        curr = request.form['curr']
    return render_template('product_detail.html', product=product, cate_id=cate_id, products=products,
                           category_name=category_name, i=i, size=size)


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


@app.route("/api/cart", methods=['post'])
def add_to_cart():
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}
    # lay 1 dictionary
    data = request.json
    message = 'Thêm thành công {} sản phẩm!'.format(data['quantity'])
    id = str(data['id'])
    if id in cart:
        # Check if user can add more book
        cart_quantity = cart[id]['quantity']
        if cart_quantity + data['quantity'] <= data['quantity_in_stocks']:
            cart[id]['quantity'] += data['quantity']
        else:
            message = 'Quá số lượng tồn kho'
    else:
        if data['quantity'] <= data['quantity_in_stocks']:
            name = data['book_name']
            price = data['unit_price']
            image = data['image']
            quantity_in_stocks = data['quantity_in_stocks']
            quantity = data['quantity']
            cart[id] = {
                "id": id,
                "book_name": name,
                "unit_price": price,
                "quantity": quantity,
                'image': image,
                "quantity_in_stocks": quantity_in_stocks
            }

        else:
            message = 'Quá số lượng tồn kho'
    # session luu lai key va value
    session[key] = cart
    # Tra ve 1 doi tuong dictionary
    return jsonify(utils.cart_stats(cart, message=message))


@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    message = 'Xóa thành công'
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart, message=message))


# product_id (string type)
@app.route('/api/cart/<product_id>', methods=['put'])
def update_cart(product_id):
    message = ''
    key = app.config['CART_KEY']
    cart = session.get(key)
    if cart and product_id in cart:
        input_quantity = int(request.json['quantity'])
        if input_quantity <= cart[product_id]['quantity_in_stocks']:
            cart[product_id]['quantity'] = input_quantity
        else:
            # gán lại bằng giá trị tối đa trong tồn kho
            cart[product_id]['quantity'] = cart[product_id]['quantity_in_stocks']
    session[key] = cart
    return jsonify(utils.cart_stats(cart, message=message))


@app.route('/api/pay')
@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart:
        try:
            dao.save_receipt(cart=cart)
        except Exception as ex:
            print(str(ex))
            return jsonify({"status": 500})
        else:
            del session[key]

    return jsonify({"status": 200})


@app.route("/cart_details")
def cart_view():
    return render_template('cart_detail.html')


@app.context_processor
def common_attr():
    return {
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']), message='')
    }


# Chạy trang web
if __name__ == '__main__':
    app.run(debug=True)
    # Cờ debug bật để kiểm tra lỗi, triển khai lên sever phải tắt đi

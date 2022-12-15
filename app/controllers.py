# Định tuyến tới biến app trang init.py
import requests

from app.admin import InputBooksView
from app.models import UserRole
from app import app, dao, login, utils, admin as ad
# Import render_template để dùng render_template
from flask import render_template, redirect, session, jsonify, make_response
# Dùng request để đổ product theo cate_id
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app.decorator import annonymous_user
import cloudinary
import cloudinary.uploader


# Định nghĩa đường dẫn
def home():
    # số sản phẩm hiện trong 1 trang
    max_product_card = 8

    # Đổ dữ liệu category
    error_message = None
    products = list(dao.load_books())
    categories = []
    cate_id = request.args.get("category_id")
    try:
        products = dao.load_books(cate_id=cate_id)
        categories = dao.load_categories()
    except:
        error_message = 'Hệ thống bảo trì'

    page_count = int(len(products) / max_product_card)
    if len(products) % max_product_card != 0:
        page_count = page_count + 1

    best_seller = dao.select_top_best_seller(8)
    best_cate = dao.select_top_category(4)

    return render_template('index.html', categories=categories, count=0, products=products, error_message=error_message,
                           product_length=len(products), page_count=page_count, max_product_card=int(max_product_card),
                           best_seller=best_seller, best_cate=best_cate)


# Chuyển trang product
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
                           sort_value=sort_value, product_count=len(products))


# Cấu hình trang chi tiết sản phẩm
def product_detail(book_id):
    product = dao.get_book_by_id(book_id)
    category_name = dao.get_category_name(book_id)
    return render_template('product_detail.html', product=product, category_name=category_name)


def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    # nếu có tồn tại user khớp với username và password
    if user and user.user_role == UserRole.ADMIN:
        login_user(user=user)
    return redirect('/admin')


# register người dùng
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['repassword']
        if password.__eq__(confirm):
            if dao.check_user_name(request.form['username']):
                err_msg = 'Tên tài khoản đã tồn tại'
            elif dao.check_phone_number(request.form['phone_number']):
                err_msg = 'Số điện thoại đã tồn tại'
            else:
                if request.files:
                    try:
                        res = cloudinary.uploader.upload(request.files['avatar'])
                        avatar = res['secure_url']
                    except Exception as ex:
                        print(ex)
                        avatar = app.config['DEFAULT_AVATAR']
                else:
                    avatar = app.config['DEFAULT_AVATAR']
                try:
                    dao.register(name=request.form['name'],
                                 username=request.form['username'],
                                 phone=request.form['phone_number'],
                                 password=password,
                                 avatar=avatar)
                    return redirect('/login')
                except Exception as ex:
                    print(ex)
                    err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau"
        else:
            err_msg = 'Mật khẩu không khớp'
    return render_template("register.html", err_msg=err_msg)


# login người dùng
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get("next")
            return redirect(n if n else '/')
    return render_template('login.html')


# logout
@login_required
def logout_my_user():
    logout_user()
    return redirect('/')


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


def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)
    message = 'Đã xóa thành công {}'.format(cart[product_id]['book_name'])
    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart, message=message))


def update_cart(product_id):
    message = 'Cập nhật giỏ hàng thành công!'
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


@login_required
def pay():
    # ghi nhận hóa đơn
    key = app.config['CART_KEY']
    cart = session.get(key)
    order_id = -1
    if cart:
        try:
            order_id = dao.save_receipt(cart=cart, address=str(request.json['address']),
                                        status=bool(request.json['status']))
        except Exception as ex:
            print(str(ex))
            return jsonify({
                "status": 500,
                "message": "Hệ thống gặp lỗi",
            })
        else:
            del session[key]

    return jsonify({
        "status": 200,
        "message": "Hoàn tất thanh toán",
    })


def pay_with_momo():
    # response = requests.
    # print(response)
    # gọi /api/pay thành công mới gọi đến /api/payWithMoMo
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    # order_id = request.json['order_id']
    # books = dao.load_book_by_order_id(order_id=order_id)
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}
    if cart:
        amount = 0
        for c in cart.values():
            amount += int(c['unit_price']) * int(c['quantity'])
        redirect_url = request.url_root + 'api/momo_result'
        ipn_url = request.url_root + 'api/momo_result'
        info = {
            'redirect_url': redirect_url,
            'ipn_url': ipn_url,
            'amount': amount,
            'user_info': {
                'name': current_user.name
            },
            'order_info': str(request.json['address'])
        }
        data = utils.get_pay_url(info)
        length = len(data)
        # print(data)
        response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json',
                                                               'Content-Length': str(length)})
        print(response.json())
        return jsonify(response.json())


def momo_result():
    # response = make_response('', 204)
    if int(request.args['resultCode']) == 0:
        dao.save_receipt(session['cart'], str(request.args['orderInfo']), True)
        del session['cart']
    return redirect('/cart_details')


def cart_view():
    return render_template('cart_detail.html')


def checkout():
    return render_template('checkout.html')


@login_required
def user_orders_view():
    orders = dao.get_orders(current_user.id)
    order_details = {}
    # order_details = {
    #       1 : [...],
    #       2 : [...]
    # }
    for o in orders:
        order_details[o.id] = dao.get_order_details(o.id)
    # print(orders)
    # print(order_details)
    return render_template('orders_view.html', orders=orders, order_details=order_details)

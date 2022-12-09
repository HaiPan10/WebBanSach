# Đọc json
import json
# Lấy đường dẫn tuyệt đối
import os
from app import app


# Hàm đọc json
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def write_json(path, file):
    with open(os.path.join(app.root_path, path), "w") as f:
        json.dump(file, f)


# Đọc category
def load_categories():
    return read_json(os.path.join(app.root_path, 'data/categories.json'))


# Đọc product
def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
    products = read_json(os.path.join(app.root_path, 'data/products.json'))

    # Đoạn này sẽ sửa đổi sau
    if cate_id:
        products = [p for p in products if p['category_id'] == int(cate_id)]

    if kw:
        products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]

    if from_price:
        products = [p for p in products if p['price'] >= float(from_price)]

    if to_price:
        products = [p for p in products if p['price'] <= float(to_price)]

    return products;


# Lấy products từ mã
def get_product_by_id(product_id):
    products = read_json(os.path.join(app.root_path, 'data/products.json'))
    for p in products:
        if p['id'] == product_id:
            return p


def read_rules():
    return read_json(os.path.join(app.root_path, 'data/adjust_rules.json'))


def cart_stats(cart, message):
    # Kiem tra tinh trang cua cart
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['unit_price']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'message': message,
    }

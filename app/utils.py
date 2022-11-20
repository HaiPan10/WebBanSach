# Đọc json
import json
# Lấy đường dẫn tuyệt đối
import os
from app import app


# Hàm đọc json
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


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
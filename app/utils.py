# Đọc json
import json
# Lấy đường dẫn tuyệt đối
import os
from app import  app


# Hàm đọc json
def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


# Đọc category
def load_categories():
    return read_json(os.path.join(app.root_path, 'data/categories.json'))


# Đọc product
def load_products():
    return read_json(os.path.join(app.root_path, 'data/products.json'))

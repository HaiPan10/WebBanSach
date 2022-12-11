# Đọc json
import hashlib
import hmac
import json
# Lấy đường dẫn tuyệt đối
import os
import uuid

import requests

from app import app, dao


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


def get_pay_url(info):
    partnerCode = "MOMO"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "pay with MoMo"
    requestId = str(uuid.uuid4())
    orderId = str(uuid.uuid4())
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString
    rawSignature = "accessKey=" + accessKey + "&amount=" + str(int(info['amount'])) + "&extraData=" + extraData + \
                   "&ipnUrl=" + info['ipn_url'] + "&orderId=" + orderId + "&orderInfo=" + orderInfo + \
                   "&partnerCode=" + partnerCode + "&redirectUrl=" + info['redirect_url'] + "&requestId=" + \
                   requestId + "&requestType=" + requestType
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': str(int(info['amount'])),
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': info['redirect_url'],
        'ipnUrl': info['ipn_url'],
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature,
        'userInfo': info['user_info']
    }
    # print(data)
    return json.dumps(data)

# Định tuyến tới biến app trang init.py
from app import app
# Import render_template để dùng render_template
from flask import render_template
# Import modul utils để dùng hàm load_
import utils
# Dùng request để đổ product theo cate_id
from flask import  request


# Định nghĩa đường dẫn
@app.route("/")
def home():
    # Đổ dữ liệu category
    cates = utils.load_categories()
    return render_template('index.html', categories=cates)


# Chuyển trang product
@app.route("/products")
def product_list():
    #Đổ dữ liệu theo cate_id
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.load_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('products.html', products=products)


# Cấu hình trang chi tiết sản phẩm
@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)

    return  render_template('product_detail.html', product=product)


# Chạy trang web
if __name__ == '__main__':
    app.run(debug=True)
    # Cờ debug bật để kiểm tra lỗi, triển khai lên sever phải tắt đi



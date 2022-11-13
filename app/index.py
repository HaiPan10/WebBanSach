# Định tuyến tới biến app trang init.py
from app import app
# Import render_template để dùng render_template
from flask import render_template
# Import modul utils để dùng hàm load_
import  utils


# Định nghĩa đường dẫn
@app.route("/")
def home():
    # Đổ dữ liệu
    cates = utils.load_categories()
    return render_template('index.html',
                           categories = cates)


# Chuyển trang product
@app.route("/products")
def product_list():
    return render_template('products.html')


# Chạy trang web
if __name__ == '__main__':
    app.run(debug=True)
    # Cờ debug bật để kiểm tra lỗi, triển khai lên sever phải tắt đi



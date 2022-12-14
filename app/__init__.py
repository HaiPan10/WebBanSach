# Khởi tạo packet
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
from flask_babelex import Babel

# Khởi tạo packet
app = Flask(__name__)
app.secret_key = 'ahdfpiwqeuiqudasdasdncblzbvjlhajz,nfm,sandkqwpuep'

# Cau hinh database trong day
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6582479:REVLUdhU9S@sql6.freemysqlhosting.net' \
                                        '/sql6582479?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
cloudinary.config(
    cloud_name='dxjkpbzmo',
    api_key='728767975167981',
    api_secret='XG9MHhjvkixgZcRfriKwyXSEqjM'
)
db = SQLAlchemy(app=app)
# Khai báo 1 đối tượng login mananger để quản lý login
login = LoginManager(app=app)

# Dịch admin sang tiếng Việt
babel = Babel(app=app)

# thiet lap cart key
app.config['CART_KEY'] = 'cart'
# Thiet lap chuoi default avatar
app.config['DEFAULT_AVATAR'] = 'https://res.cloudinary.com/dxjkpbzmo/image/upload/v1669580265/b8ojpgctmqsnmoyju7cp.png'


@babel.localeselector
def load_locale():
    return 'vi'

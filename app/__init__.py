# Khởi tạo packet
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary


# Khởi tạo packet
app = Flask(__name__)
app.secret_key = 'ahdfpiwqeuiqudasdasdncblzbvjlhajz,nfm,sandkqwpuep'

#Cau hinh database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6580990:Kkw1S1JuMU@sql6.freemysqlhosting.net' \
                                        '/sql6580990?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)
# Khai báo 1 đối tượng login mananger để quản lý login
login = LoginManager(app=app)

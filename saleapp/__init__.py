from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key = '4567890sdfghjklcvbnvb4567fg6yug'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/test?charset=utf8mb4' % quote('123456789')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(
  cloud_name = "djmsbhhnn",
  api_key = "882934827235495",
  api_secret = "B_W1dvsyB8A8DoBjatIz_tE5orw"
)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return "vi"

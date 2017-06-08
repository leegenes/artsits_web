from flask import Flask

app = Flask(__name__)
# app.secret_key = '92+XthJw=KA&3fKjuwB3P/c+4*{+mDPG8cZ'
app.config['SECRET_KEY'] = '92+XthJw=KA&3fKjuwB3P/c+4*{+mDPG8cZ'
from app import views

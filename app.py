from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/dbis-practice"
#app.config['SECRET_KEY'] = '38c0408496b1aafc76a1278296c25137'

""""""
uri = os.environ['DATABASE_URL']
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = "key"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

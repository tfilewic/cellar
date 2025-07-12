from flask import Flask
from models import db
from flasgger import Swagger

app = Flask(__name__)
app.config.from_pyfile("../config.py")
db.init_app(app)
swagger = Swagger(app)

from app import routes

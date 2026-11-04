from http import HTTPStatus

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from yacut import views
from yacut import error_handlers

app.register_error_handler(
    HTTPStatus.NOT_FOUND,
    error_handlers.page_not_found
)

from yacut import api_views

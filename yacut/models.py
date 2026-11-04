from datetime import datetime

from yacut import db
from yacut.constants import (
    MAX_CUSTOM_ID_LENGTH,
    MAX_ORIGINAL_URL_LENGTH,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(MAX_ORIGINAL_URL_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(MAX_CUSTOM_ID_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )

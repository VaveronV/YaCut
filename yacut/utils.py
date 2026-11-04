
import random
import string

from yacut import db
from yacut.constants import SHORT_ID_LENGTH
from yacut.models import URLMap


CHARACTERS = string.ascii_letters + string.digits


def get_unique_short_id():
    while True:
        short_id = ''.join(
            random.choices(CHARACTERS, k=SHORT_ID_LENGTH)
        )
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def create_url_map(original, custom_id=None):
    short = custom_id or get_unique_short_id()

    url_map = URLMap(
        original=original,
        short=short
    )
    db.session.add(url_map)
    db.session.commit()

    return url_map

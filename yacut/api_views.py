
import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import (
    DUPLICATE_ERROR,
    MAX_CUSTOM_ID_LENGTH,
    RESERVED_SHORT_ID,
)
from yacut.models import URLMap
from yacut.utils import create_url_map


SHORT_ID_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            'message': 'Отсутствует тело запроса'
        }), HTTPStatus.BAD_REQUEST

    original = data.get('url')
    custom_id = data.get('custom_id')

    if custom_id == '':
        custom_id = None

    if not original:
        return jsonify({
            'message': '"url" является обязательным полем!'
        }), HTTPStatus.BAD_REQUEST

    if custom_id is not None:
        if (
            not isinstance(custom_id, str)
            or not SHORT_ID_PATTERN.fullmatch(custom_id)
            or len(custom_id) > MAX_CUSTOM_ID_LENGTH
        ):
            return jsonify({
                'message': 'Указано недопустимое имя для короткой ссылки'
            }), HTTPStatus.BAD_REQUEST

        if (
            custom_id == RESERVED_SHORT_ID
            or URLMap.query.filter_by(short=custom_id).first()
        ):
            return jsonify({
                'message': DUPLICATE_ERROR
            }), HTTPStatus.BAD_REQUEST

    url_map = create_url_map(original, custom_id)

    return jsonify({
        'url': url_map.original,
        'short_link': request.host_url.rstrip('/') + '/' + url_map.short
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()

    if url_map is None:
        return jsonify({
            'message': 'Указанный id не найден'
        }), HTTPStatus.NOT_FOUND

    return jsonify({
        'url': url_map.original
    }), HTTPStatus.OK


from http import HTTPStatus

import aiohttp

from yacut import app


YANDEX_DISK_FOLDER = 'YaCut'
YANDEX_DISK_API = 'https://cloud-api.yandex.net/v1/disk/resources'
UPLOAD_URL = f'{YANDEX_DISK_API}/upload'
PUBLISH_URL = f'{YANDEX_DISK_API}/publish'

OVERWRITE_EXISTING = 'true'


async def upload_file(file, filename):
    """Загружает файл на Яндекс Диск и получает публичную ссылку."""
    token = app.config['DISK_TOKEN']

    headers = {
        'Authorization': f'OAuth {token}'
    }

    async with aiohttp.ClientSession() as session:
        # Создаём папку.
        async with session.put(
            YANDEX_DISK_API,
            headers=headers,
            params={'path': YANDEX_DISK_FOLDER}
        ) as response:
            if response.status not in (
                HTTPStatus.CREATED,
                HTTPStatus.CONFLICT
            ):
                response.raise_for_status()

        # Получаем ссылку для загрузки.
        params = {
            'path': f'{YANDEX_DISK_FOLDER}/{filename}',
            'overwrite': OVERWRITE_EXISTING
        }

        async with session.get(
            UPLOAD_URL,
            headers=headers,
            params=params
        ) as response:
            response.raise_for_status()
            upload_url = (await response.json())['href']

        # Загружаем файл.
        async with session.put(
            upload_url,
            data=file
        ) as response:
            response.raise_for_status()

        # Делаем файл публичным.
        async with session.put(
            PUBLISH_URL,
            headers=headers,
            params={
                'path': f'{YANDEX_DISK_FOLDER}/{filename}'
            }
        ) as response:
            response.raise_for_status()

        # Получаем публичную ссылку.
        async with session.get(
            YANDEX_DISK_API,
            headers=headers,
            params={
                'path': f'{YANDEX_DISK_FOLDER}/{filename}',
                'fields': 'public_url'
            }
        ) as response:
            response.raise_for_status()
            public_url = (await response.json()).get('public_url')

    if not public_url:
        raise ValueError('Не удалось получить публичную ссылку на файл')

    return public_url

import aiohttp

from yacut import app


YANDEX_DISK_FOLDER = 'YaCut'
YANDEX_DISK_API = 'https://cloud-api.yandex.net/v1/disk/resources'
UPLOAD_URL = f'{YANDEX_DISK_API}/upload'
DOWNLOAD_URL = f'{YANDEX_DISK_API}/download'

OVERWRITE_EXISTING = 'true'


async def upload_file(file, filename):
    """Загружает файл на Яндекс Диск и возвращает ссылку на скачивание."""
    token = app.config['DISK_TOKEN']
    headers = {'Authorization': f'OAuth {token}'}
    disk_path = f'{YANDEX_DISK_FOLDER}/{filename}'

    async with aiohttp.ClientSession() as session:
        async with session.get(
            UPLOAD_URL,
            headers=headers,
            params={
                'path': disk_path,
                'overwrite': OVERWRITE_EXISTING
            }
        ) as response:
            response.raise_for_status()
            upload_url = (await response.json())['href']

        file.seek(0)

        async with session.put(
            upload_url,
            data=file.read()
        ) as response:
            response.raise_for_status()

        async with session.get(
            DOWNLOAD_URL,
            headers=headers,
            params={'path': disk_path}
        ) as response:
            response.raise_for_status()
            download_url = (await response.json())['href']

    return download_url

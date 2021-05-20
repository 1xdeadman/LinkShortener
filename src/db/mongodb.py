from typing import Optional


from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from flask import current_app, g


from src.helpers import create_url_entity


def _get_db() -> Database:
    if 'db' not in g:
        if current_app.config.get("DB_CERT_PATH") == "":
            client = MongoClient(current_app.config.get("DB_URL"))
        else:
            raise NotImplemented("логика подключения по TLS")
        g.db = client[current_app.config.get('DB_NAME')]
    return g.db


def _get_urls() -> Collection:
    return _get_db()[current_app.config.get('DB_URL_COLLECTION')]


def add_new_url(long_url: str) -> Optional[bytes]:
    """
    Добавляет новый адрес в базу

    :param long_url: полный адрес
    :return: сокращенный адрес
    """
    try:
        urls = _get_urls()
        res = urls.insert_one(create_url_entity(long_url=long_url))
        if res.acknowledged is True:
            number = res.inserted_id.binary
            return number
        return None
    except Exception:
        return None


def remove_url_by_short_url(short_url: bytes) -> bool:
    """
    Удалить полную ссылку

    :param short_url: короткая ссылка, соотнесенная с полной
    :return:
    True - если удалены было успешно, иначе False
    """
    try:
        urls = _get_urls()
        res = urls.delete_one(
            filter=create_url_entity(short_url)
        )
        return res.acknowledged is True and res.deleted_count == 1
    except Exception:
        return False


def get_long_url(short_url: bytes) -> Optional[str]:
    """
    Получить полный url по сокращенному
    :param short_url: сокращенный гкд
    :return: полный url
    """
    try:
        urls = _get_urls()
        res = urls.find_one(
            filter=create_url_entity(short_url)
        )
        return res['long_url']
    except Exception:
        return None

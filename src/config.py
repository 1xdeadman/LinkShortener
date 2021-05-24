import os
from flask import Config


class ProductionConfig(Config):
    DB_URL: str = os.environ.get('DB_URL') or \
                  "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    DB_NAME: str = os.environ.get('DB_NAME') or "linkShortener"
    DB_URL_COLLECTION: str = os.environ.get('DB_URL_COLLECTION') or "urls"
    DB_CERT_PATH: str = ""
    BASE_PATH: str = os.environ.get('BASE_URL') or 'http://127.0.0.1:5000/'
    API_SCHEMA: dict = dict()
    JSON_AS_ASCII: bool = False


class DebugConfig(ProductionConfig):
    DB_CERT_PATH = ""

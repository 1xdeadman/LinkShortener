from typing import Optional, Any
from json import load

from flask import Flask


class ApiSchema:
    def __init__(self, app: Optional[Flask] = None):
        self._app: Flask = app

    def init_app(self, app: Flask):
        self._app: Flask = app

    def find_url(self, rel: str) -> Optional[str]:
        for i in range(len(self._app.config['API_SCHEMA']['resources'])):
            if self._app.config['API_SCHEMA']['resources'][i]['rel'] == rel:
                return self._app.config['API_SCHEMA']['resources'][i]['href']

    def _set_value(self, rel: str, key: str, value: Any):
        for i in range(len(self._app.config['API_SCHEMA']['resources'])):
            if self._app.config['API_SCHEMA']['resources'][i]['rel'] == rel:
                self._app.config['API_SCHEMA']['resources'][i][key] = value

    def create_schema(self):
        self._app.config['API_SCHEMA'] = load(open('api_schema.json', 'r', encoding='utf-8'))

        self._set_value('home', 'href', self._app.config.get('BASE_URL') or 'http://127.0.0.1:5000/')
        self._set_value('base_uri', 'href', self._app.config.get('BASE_URL') or 'http://127.0.0.1:5000/')
from typing import Optional, Any
from json import load

from flask import Flask


CONFIG_PARAM = 'API_SCHEMA'


def find_url(app: Flask, rel: str) -> Optional[str]:
    for i in range(len(app.config[CONFIG_PARAM]['resources'])):
        if app.config[CONFIG_PARAM]['resources'][i]['rel'] == rel:
            return app.config[CONFIG_PARAM]['resources'][i]['href']


def _set_value(app: Flask, rel: str, key: str, value: Any):
    for i in range(len(app.config[CONFIG_PARAM]['resources'])):
        if app.config[CONFIG_PARAM]['resources'][i]['rel'] == rel:
            app.config[CONFIG_PARAM]['resources'][i][key] = value


def create_schema(app: Flask):
    try:
        app.config[CONFIG_PARAM] = load(open('src/api_schema.json', 'r', encoding='utf-8'))
    except Exception:
        app.config[CONFIG_PARAM] = load(open('api_schema.json', 'r', encoding='utf-8'))
    print(app.config[CONFIG_PARAM])

    _set_value(app, 'home', 'href', app.config.get('BASE_URL') or 'http://127.0.0.1:5000/')
    _set_value(app, 'base_uri', 'href', (app.config.get('BASE_URL') or 'http://127.0.0.1:5000/') + 'api/')


def get_api_schema(app: Flask):
    return app.config[CONFIG_PARAM]

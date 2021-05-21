from json import load
from base64 import urlsafe_b64decode

from flask import Flask, jsonify, redirect, abort

from src.db import get_long_url
from src.config import DebugConfig as Config


api_schema = load(open('api_schema.json', 'r', encoding='utf-8'))


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from src.api import bp
    app.register_blueprint(bp)

    import src.db

    @app.route('/')
    def get():
        response = jsonify(api_schema)
        response.content_type = "application/json; charset=utf-8"
        return response

    @app.route('/urls/<short_url>')
    def redirect_to_url(short_url: str):
        long_url = get_long_url(urlsafe_b64decode(short_url))
        if long_url is not None:
            return redirect(long_url)
        return abort(404)

    return app

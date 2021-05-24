from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Optional

from flask import request

from src.api import bp
from src.app import apiSchema
from src.db import get_long_url, add_new_url, remove_url_by_short_url
from src.helpers import create_failure_response, create_url_response


@bp.route('/create/', methods=["POST"])
def create_short_url():
    """
    Обрабатывает запрос на создание новой сокращенной ссылки.

    :return:
    """
    if 'long_url' not in request.json:
        return create_failure_response(code="1", message="Неправильные параметры запроса")

    long_url = request.json['long_url']

    tmp = add_new_url(long_url)
    if tmp is None:
        return create_failure_response(code="0", message="Неизвестная ошибка")

    short_number = urlsafe_b64encode(tmp).decode(encoding='utf-8')
    return create_url_response(
        short="{0}urls/{1}".format(apiSchema.find_url('home'), short_number),
        long=long_url)


@bp.route('/remove/', methods=['DELETE'])
def remove_url():
    """
    Обрабатывает запрос на удаление сокращенной ссылки.

    :return:
    """
    if 'short_url' not in request.json:
        return create_failure_response(code="1", message="Неправильные параметры запроса")

    short_url = request.json['short_url']
    short_url = short_url.replace('\\', '/')

    try:
        bin_url = urlsafe_b64decode(short_url.rstrip('/').split('/')[-1])
    except:
        return create_failure_response(code="1", message="Неправильные параметры запроса")

    long_url = get_long_url(bin_url)
    if long_url is None:
        return create_failure_response(code='2', message='Не найден удаляемый url')
    res = remove_url_by_short_url(bin_url)
    if res:
        return create_url_response(short=short_url, long=long_url)
    else:
        return create_failure_response(code='0', message='Неизвестная ошибка')

from typing import Optional, Any

import requests
import click


_api_schema = None
actions = {}
url = None


def get_api_schema():
    """
    Получает схему api

    :return:
    """
    global _api_schema
    global url
    if _api_schema is None:
        if url is None:
            url = input("Введите адрес сервиса [Пример: 'http://localhost:5000/']: ")  # 'http://localhost:5000/'
        res = requests.get(url)
        if res.status_code == 200:
            _api_schema = res.json()
    return _api_schema


def get_action(action: str) -> Optional[dict[str, Any]]:
    """
    Ищет объект, описывающий действие <action>

    :param action: искомое действие
    :return: словарь, описывающий желаемое действие
    """
    if actions.get(action) is None:
        api_schema = get_api_schema()
        for i in range(len(api_schema['resources'])):
            if api_schema['resources'][i]['rel'] == action:
                actions[action] = api_schema['resources'][i]
                return api_schema['resources'][i]
        return None
    else:
        return actions[action]


def get_base_action() -> Optional[dict[str, Any]]:
    """
    Получает объект, описывающий точку входа в апи

    :return:
    """
    api_schema = get_api_schema()
    for i in range(len(api_schema['resources'])):
        if api_schema['resources'][i]['rel'] == 'base_uri':
            return api_schema['resources'][i]
    return None


def get_href(action: str) -> str:
    """
    Ищет ссылку для осушествления действия <action>

    :param action: искомое действие
    :return: ссылка на ресурс, осущесвляющий желаемое действие
    """

    res = get_base_action()['href'] + get_action(action)['href']

    return res


def get_method(action: str) -> str:
    return get_action(action)['method']


def get_body_params(action: str) -> tuple[str, list[dict[str, str]]]:
    """
    :param action:
    :return: Возвращает кортеж из MIME типа и списка параметров
    """
    return get_action(action)['body']["application/json"], get_action(action)['body']["param_list"]


@click.group()
def run():
    pass


@run.command()
@click.option('--long_url', '-l', type=str, required=True)
def create_short_url(long_url: str):
    href = get_href('create_url')
    params = dict()
    params['long_url'] = long_url

    res = requests.post(href, json=params)
    if res.status_code == 200 and res.json()['status'] == 'success':
        print(res.json()['body']['short'])
    else:
        print(res.json()['body'])


@run.command()
@click.option('--short_url', '-s', type=str, required=True)
def remove_short_url(short_url: str):
    href = get_href('remove_url')
    params = dict()
    params['short_url'] = short_url

    res = requests.delete(href, json=params)
    if res.status_code == 200 and res.json()['status'] == 'success':
        print(res.json()['body']['short'])
    else:
        print(res.json()['body'])


if __name__ == '__main__':
    run()

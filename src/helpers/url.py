from bson import ObjectId


class UrlFields:
    SHORT = 'short_url'
    LONG = 'long_url'


def create_url_entity(short_url: bytes = None, long_url: str = None):
    if long_url is not None:
        return {
            UrlFields.LONG: long_url
        }
    return {
        "_id": ObjectId(short_url)
    }

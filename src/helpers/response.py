class Status:
    FAILURE = "failure"
    SUCCESS = "success"


def create_response(status: str, body: dict[str, str]):
    return {
        "status": status,
        "body": body
    }


def create_success_response(body: dict[str, str]):
    return create_response(Status.SUCCESS, body)


def create_url_response(short: str, long: str):
    return create_success_response({
        "short": short,
        "long": long
    })


def create_failure_response(code: str, message: str):
    return create_response(Status.FAILURE, {"code": code, "message": message})

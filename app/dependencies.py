from fastapi import Request


def get_comic_service(request: Request):
    return request.app.state.comic_service
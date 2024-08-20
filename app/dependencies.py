from fastapi import Request


async def check_request_server(request: Request):
    # check request.client.host
    return True

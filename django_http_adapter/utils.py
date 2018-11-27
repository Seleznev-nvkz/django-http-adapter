from importlib import import_module


def get_module_attr(path: str):
    """ getter for path like user.model.User or user.model.User:init """

    module, attr = path.rsplit('.', 1)
    if ':' in attr:
        cls, method = attr.split(':')
        return getattr(getattr(import_module(module), cls), method)
    return getattr(import_module(module), attr)


def send_data_by_http(data: dict, receiver: str, server_id: int, thread: bool = True):
    """ send data to receiver by server_id """

    from django_http_adapter.client import http_adapter_clients

    data['receiver'] = receiver
    return http_adapter_clients[server_id].send(data, thread)

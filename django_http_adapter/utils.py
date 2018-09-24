from importlib import import_module


def get_module_attr(path):
    """ getter for path like user.model.User or user.model.User:init """

    module, attr = path.rsplit('.', 1)
    if ':' in attr:
        cls, method = attr.split(':')
        return getattr(getattr(import_module(module), cls), method)
    return getattr(import_module(module), attr)

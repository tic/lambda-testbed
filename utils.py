
def default_context():
    return {
        'body-json': {},
        'params': {
            'path': {},
            'query': {},
        }
    }

def simple_context(path_params=[], query_params=[], body_params=[], custom_params=[]):
    base = default_context()
    for param in path_params:
        base['params']['path'][param['name']] = param['value']

    for param in query_params:
        base['params']['query'][param['name']] = param['value']

    for param in path_params:
        base['body-json'][param['name']] = param['value']

    for param in custom_params:
        base[param['name']] = param['value']

    return base

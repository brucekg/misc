# This module provides methods that add functionality to objects.
# These functions maybe called directly with the first argument being the given object or maybe bound to a class.


def get_dict(given, block=None, only=None, private=False):
    if given is None:
        return None

    """
    This function/method recursively produces a dictionary from the given object in accordance with the parameters.

    :param given: an object with attributes, maybe a dict
    :param block: list of attributes to be blocked
    :param only: list of attributes to be in returned dictionary
    :param private: if False block private attributes - startswith('_')
    :return: a new complete data dictionary
    """
    if block is None:
        block = []

    d = dict()
    if type(given) is dict:
        given_dict = given
    else:
        given_dict = given.__dict__

    for k in given_dict:
        if _get_dict_allow(k, block, only, private):
            v = given_dict[k]
            if 'get_dict' in dir(v.__class__):
                v = v.get_dict(block=block, only=only, private=private)
            else:
                if type(v) is list:
                    d_list = []
                    for element in v:
                        assert element is not list, 'get_dict does not support list in list'
                        if 'get_dict' in dir(element.__class__):
                            w = element.get_dict(block=block, only=only, private=private)
                        elif element is dict or getattr(element, '__dict__', None):
                            w = get_dict(element, block=block, only=only, private=private)
                        else:
                            w = element
                        d_list.append(w)
                    v = d_list
                elif type(v) is dict:
                    v = get_dict(v, block=block, only=only, private=private)
            d[k] = v
    return d


def _get_dict_allow(key, block, only, private):
    """
    This function determines is a dictionary element should be blocked given its key and the screening parameters.

    :param key: a string
    :param block: list of attributes to be blocked
    :param only: list of attributes to be in returned dictionary
    :param private: if False block private attributes - startswith('_')
    :return: True if allowed, False if screened
    """

    if only:
        # only allow the only listed keys
        return bool(key in only)

    if block and key in block:
        # block the block listed keys
        return False

    # allow key if private is allowed
    # private keys are not allowed if private is False
    # any key that is prefixed with an underscore is private
    return private or not key.startswith('_')

def update(given, *args, **kwargs):
    """
    This method updates the object attributes.  This is used by __init__.

    :param args: an arg maybe an object, a dict, or a json string.
    :param kwargs: a kwarg specifies the keyword and value of an attribute to be updated or initialized.
    :return: nothing
    """
    for arg in args:
        if arg is None:
            pass
        elif type(arg) is dict:
            given.__dict__.update(arg)
        elif type(arg) is str:
            d = json.loads(arg)
            given.__dict__.update(d)
        else:
            given.__dict__.update(arg.__dict__)
    given.__dict__.update(**kwargs)
    return

def json(given, **kwargs):
    """
    This method produces a json string for the objects.

    :param kwargs: passed to json.dumps() - example x.json_(indent=3) for pretty indented output
    :return: json document string
    """
    j = json.dumps(given.__dict__, **kwargs)
    return j

def is_empty(given):
    return len(given.__dict__) == 0


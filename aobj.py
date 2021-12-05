import json

from object_methods import get_dict


class AObj(object):
    """
    An object subclass that provides attribute access.

    AObj provides attribute access (dot notation).  Attribute get, set, and del are supported.
    The methods provided by this class all are named with a trailing underscore to avoid reserving
    any attribute names.
    """
    def __init__(self, *args, **kwargs):
        """
        The initialize object method.

        This method can be given arguments and kwargs which are used to update the objects attributes.
        See the update_ method for specifics.
        """
        self.update_(*args, **kwargs)
        return

    def update_(self, *args, **kwargs):
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
                self.__dict__.update(arg)
            elif type(arg) is str:
                d = json.loads(arg)
                self.__dict__.update(d)
            else:
                self.__dict__.update(arg.__dict__)
        self.__dict__.update(**kwargs)
        return

    def json_(self, **kwargs):
        """
        This method produces a json string for the objects.

        :param kwargs: passed to json.dumps() - example x.json_(indent=3) for pretty indented output
        :return: json document string
        """
        j = json.dumps(self.__dict__, **kwargs)
        return j

    def is_empty(self):
        return len(self.__dict__) == 0

    @classmethod
    def create(cls, *args, **kwargs):
        """
        This method returns an object like __init__ except that is if args is an empty list or are all None and kwargs
        is empty then None is returned.

        :param args:
        :param kwargs:
        :return:
        """
        empty_none = True
        if kwargs:
            # any keyword arguments
            empty_none = False
        else:
            # any arguments that are not None
            for arg in args:
                if arg is not None and arg != 'None':
                    empty_none = False
                    break
        if empty_none:
            return None
        return AObj(*args, **kwargs)

    def dict_(self, screen=None):
        return get_dict(self, block=screen)

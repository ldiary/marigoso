import time


class BuiltIn(object):

    def delstring(self, mystring, dellist):
        for deletable in dellist:
            mystring = mystring.replace(deletable, "")
        return mystring

    def wait(self, seconds):
        time.sleep(seconds)


class MutantDictionary(dict):
    """Subclass of a dictionary that allows dot syntax notation for accessing
    key value pairs.
    """
    def __init__(self, *args, **kwargs):
        super(MutantDictionary, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(MutantDictionary, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(MutantDictionary, self).__delitem__(key)
        del self.__dict__[key]

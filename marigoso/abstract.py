import time
import datetime
import pprint


class Utils(object):

    def delstring(self, mystring, dellist):
        for deletable in dellist:
            mystring = mystring.replace(deletable, "")
        return mystring

    def wait(self, seconds):
        time.sleep(seconds)

    def timestamp(self):
        now = datetime.datetime.utcnow()
        timestamp = now.strftime("_%d%m%Y_%H%M%S")
        return str(timestamp)

    def time_unique(self, whatever):
        today = datetime.datetime.utcnow()
        whatever += "_" + today.strftime('%Y-%b-%d_%H-%M-%S-%f')
        return whatever

    def day(self):
        now = datetime.datetime.utcnow()
        day = now.day
        return str(day)

    def month(self):
        now = datetime.datetime.utcnow()
        month = now.strftime("%B")
        return str(month[:3])

    def year(self):
        now = datetime.datetime.utcnow()
        year = now.year
        return str(year)

    def log(self, message):
        print(message)

    def pretty_log(self, message):
        pprint.pprint(message, indent=4)

    def trim_start(self, string, start, end=None):
        extract = string[string.find(start) + len(start):end]
        return extract.strip()


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

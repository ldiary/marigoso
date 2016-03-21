import time
import datetime
import pprint
import pathlib
import sys


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

    def timelapse(self, start, end=None, unit=None):
        if end is not None:
            duration = end - start
        else:
            duration = datetime.datetime.utcnow() - start
        days, seconds = duration.days, duration.seconds
        total_in_hrs = (days * 24) + (seconds // 3600)
        total_in_mins = (days * 1440) + (seconds // 60)
        total_in_seconds = days * 86400 + seconds
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60
        if unit is not None:
            units = {
                'days': days,
                'hrs': total_in_hrs,
                'mins': total_in_mins,
                'seconds': total_in_seconds
            }
            return units[unit]
        return days, hrs, mins, secs

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
        """ Removes the starting substring.
        :param string: The entire string.
        :param start:  The starting substring to be removed.
        :param end:    An optional point in the string, defaults to the strings ending
        :return:       A substring consists of the subsequent substring after the
                         start substring is removed, up to the specified end.
        """
        extract = string[string.find(start) + len(start):end]
        return extract.strip()

    def import_parent_folders(self, parent, subfolder=None):
        current = pathlib.Path.cwd()
        while current.name != parent:
            current = current.parent
        if subfolder:
            located_parent = str(pathlib.PurePath(current, subfolder))
        else:
            located_parent = str(current)
        sys.path.insert(0, located_parent)
        return current, located_parent



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

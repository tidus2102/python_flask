import re
import datetime as dt
from dateutil.parser import parse as parse_time
from flask.ext.babelex import gettext

required = 'required'
binary = 'binary'


_email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)


def email(value):
    if _email_re.match(value) is None:
        return False, gettext("VALIDATION_INVALID_EMAIL %(email)s", email=value)
    return True, value


def regex(pattern, flags=0):

    def match(value):
        compiled = re.compile(pattern, flags)
        if compiled.match(value) is not None:
            return True, value
        return False, "Regex mismatch: %s (found %s)" % (pattern, value)

    return match


def model(cls, field="id"):
    def func(value):
        try:
            id = int(value)
            instance = cls.query.filter(getattr(cls, field) == id).first()
            if instance is not None:
                return True, instance
            return False, gettext("VALIDATION_INVALID_MODEL %(model)s %(id)s", model=str(cls), id=value)
        except ValueError:
            return False, gettext("VALIDATION_INVALID_INTEGER %(type)s", type=type(value))
    return func


def integer(value):
    try:
        number = int(value)
        return True, number
    except ValueError:
        return False, gettext("VALIDATION_INVALID_INTEGER %(type)s", type=type(value))


def datetime(value):
    try:
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S+0000")
        result = parse_time(value)
        return True, result
    except ValueError:
        return False, gettext("VALIDATION_INVALID_DATETIME I.E: 2014-12-11T08:23:01+0000")
        # return False, 'Invalid datetime. Example: 2014-01-01T12:34:00 (found %s)' % value


def date(value):
    try:
        return True, dt.datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return False, gettext("VALIDATION_INVALID_DATE I.E: 2014-12-11")
        # return False, 'Invalid date. Example: 2000-03-31 (found %s)' % value


def min_length(size):
    def func(value):
        if len(value) < size:
            return False, gettext("VALIDATION_INVALID_MIN_LENGHT %(value)s", value=size)
            # return False, "Minimum length should be %s" % size
        return True, value
    return func


def boolean(value):
    if value == False:
        return True, False
    if value == True:
        return True, True
    return False, gettext("VALIDATION_INVALID_BOOLEAN %(value)s", value=value)

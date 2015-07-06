import decimal, simplejson
from simplejson import dumps as _dumps
from datetime import datetime, date
from app.utils import helper
import speaklater


class CustomJSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return helper.time_to_str(o)
        if isinstance(o, speaklater._LazyString):
            return unicode(o)
        if isinstance(o, decimal.Decimal):
            return str(o)
        return simplejson.JSONEncoder.default(self, o)


def dumps(obj, cls=CustomJSONEncoder, **kwargs):
    return _dumps(obj, cls=cls, *kwargs)

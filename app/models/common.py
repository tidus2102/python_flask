from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, DateTime
import pytz
from datetime import datetime
#from flask.ext.sqlalchemy import event
from app.utils import helper

db = SQLAlchemy()
db1 = SQLAlchemy()

# SQLAlchemy does not support Datetime timezone aware type
# e.g DateTime(tzinfo=pytz.UTC)
# Todo: Change all db.DateTime to UTCDateTime
class UTCDateTime(TypeDecorator):
    impl = DateTime
    def process_bind_param(self, value, engine):
        if value is not None:
            if type(value) == unicode or type(value) == str:
                value = parser.parse(value)

            if value.tzinfo is None:
                return value.replace(tzinfo=pytz.UTC)
            return value.astimezone(pytz.UTC)

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=pytz.UTC)


class Base(object):
    @staticmethod
    def update_time(mapper, connection, target):
        target.updated_at = pytz.UTC.localize(datetime.utcnow())

    @classmethod
    def __declare_last__(cls):
        # get called after mappings are completed
        # http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html#declare-last
        #event.listen(cls, 'before_update', cls.update_time)
        pass

    @classmethod
    def findById(cls, id):
        return cls.query.get(id)

    @classmethod
    def findByAttributes(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def findAllByAttributes(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    @classmethod
    def deleteByAttributes(cls, **kwargs):
        cls.query.filter_by(**kwargs).delete()

    @classmethod
    def findAllNotIn(cls, attr, list):
        return cls.query.filter(~getattr(cls, attr).in_(list))

    def markAsDelete(self):
        self.is_deleted = True

    def returnJsonByFields(self, all_fields=[], fields=[]):
        fields = all_fields if len(fields) == 0 or not helper.checkSublist(fields, all_fields) else fields
        json = {}
        for field in fields:
            json.update({field: getattr(self, field)})
        return json
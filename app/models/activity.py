from common import db, UTCDateTime, Base
#from app.models.article import Article
from app.models.notification import Notification
from flask.ext.babelex import gettext
#from sqlalchemy.event import listen
import pytz
from datetime import datetime


class Activity(Base, db.Model):
    __tablename__ = "tbl_activity"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))

    ACTION_POST = u"posted"
    action = db.Column(db.UnicodeText(), nullable=False)

    # _mapping = dict([
    #     (klass.__tablename__, klass)
    #     for klass in [
    #         Article
    #     ]])
    # model_name = db.Column(db.Enum(_mapping.keys(), native_enum=False), nullable=False)

    model_name = db.Column(db.UnicodeText())
    model_id = db.Column(db.Integer, nullable=False)
    
    #is_deleted = db.Column(db.Boolean, default=False)

    # Relations
    notifications = db.relationship('Notification', backref='activity', lazy='dynamic', foreign_keys='Notification.activity_id', order_by='Notification.id')

    ####################
    # Instance methods #
    ####################
    @property
    def model(self):
        klass = self._mapping[self.model_name]
        return klass.query.get(self.model_id)

    @model.setter
    def model(self, obj):
        self.model_name = obj.__tablename__
        self.model_id = obj.id

    def getNotiMessage(self):
        model = self.model
        msg = ''
        # if model:
        #     if isinstance(model, Article) and self.action == self.ACTION_POST:
        #         msg = gettext('New article is posted %(article_title)s', article_title=model.title)

        return msg

    def getOptionData(self):
        model = self.model
        data = None
        if model:
            # For all user
            if isinstance(model, Article) and self.action == self.ACTION_POST:
                data = model.to_json_notification()

        return data



    @classmethod
    def create(cls, user_id, action, model):
        activity = cls()

        activity.user_id = user_id
        activity.action = action
        activity.model = model

        db.session.add(activity)

        return activity

    # @staticmethod
    # def markDelete(mapper, connect, self):
    #     from flask.ext.sqlalchemy import SQLAlchemy
    #     from notification import Notification
    #
    #     db = SQLAlchemy()
    #
    #     # mark deleted for the notifications related to this activity
    #     db.session.query(Notification)\
    #         .filter(Notification.activity_id == self.id)\
    #         .update({"is_deleted": self.is_deleted})
    #
    #     db.session.commit()


# Register event to trigger when entry is updated
#listen(Activity, "after_update", Activity.markDelete)
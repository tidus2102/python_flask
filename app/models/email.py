# -*- coding: utf-8 -*-
import pytz
from common import db, UTCDateTime, Base
from datetime import datetime
from sqlalchemy.dialects import postgresql
from flask import current_app as app

class Email(Base, db.Model):
    __tablename__ = "tbl_email"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    subject = db.Column(db.UnicodeText(), nullable=False)
    content = db.Column(db.UnicodeText())

    TYPE_HTML = u"html"
    TYPE_PLAIN = u"plain"
    type = db.Column(db.Enum([TYPE_PLAIN, TYPE_HTML], native_enum=False), nullable=False, default=TYPE_HTML)

    sender_email = db.Column(db.UnicodeText(), nullable=False)
    sender_name = db.Column(db.UnicodeText())
    receiver_emails = db.Column(postgresql.ARRAY(db.UnicodeText), nullable=False)

    STATUS_SENT = u"sent"
    STATUS_FAILED = u"failed"
    status = db.Column(db.Enum([STATUS_SENT, STATUS_FAILED], native_enum=False), nullable=False, default=STATUS_SENT)


    ####################
    # Instance methods #
    ####################


    #################
    # Class methods #
    #################
    @classmethod
    def create(cls, receiver_emails, subject=None, content=None,
               sender_email=None, sender_name=None, type=TYPE_HTML):
        assert subject
        assert content
        cfg = app.config['email']
        self = cls()
        self.sender_email = sender_email or cfg.get("sender_email")
        self.sender_name = sender_name or cfg.get("sender_name")
        self.receiver_emails = receiver_emails
        self.subject = "%(subject)s" % {"subject": subject}
        self.content = content
        self.type = type
        db.session.add(self)
        return self

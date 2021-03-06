from flask.ext.sqlalchemy import models_committed
from app.models.email import Email
from app import mail
from app.models.notification import Notification
from app import noti

def wire(app):

    @models_committed.connect_via(app)
    def sendMessages(sender, changes):
        for obj, change in changes:


            if isinstance(obj, EmailMessage) and change == "insert":
                # maybeDeferred is used so that exceptions raised from
                # mail.send does not stop other emails from being sent.
                # It's probably cleaner to make sure mail.send never
                # raises an exception, (always returning a deferred
                # that succeeds/fails instead)
                # TODO: Track status of email
                # TODO: Handle errors somehow
                message = obj
                mail.send(
                    to_list=[{"email": e} for e in message.receiver_emails],
                    subject=message.subject,
                    content=message.content,
                    sender_mail=message.sender_email,
                    sender_name=message.sender_name
                )

            if isinstance(obj, Notification) and change == "insert":
                 notification = obj

                 noti.sendNoti('apns', notification.user_id, notification.getMessage(), notification.getOptionData())
                 noti.sendNoti('gcm', notification.user_id, notification.getMessage(), notification.getOptionData())
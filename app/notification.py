from flask import current_app as app
from app import apns
from app.models.user import User
from app.models.user_token import UserToken
from queue import high_queue


def sendAPNS(user_id, message):
    from flask.ext.sqlalchemy import SQLAlchemy
    db = SQLAlchemy()
    user = db.session.query(User).get(user_id)

    apns_user_tokens = user.user_tokens.filter(
        UserToken.device_token != None,
        UserToken.device_type == UserToken.DEVICE_TYPE_APNS,
        UserToken.is_active == True
    )

    if apns_user_tokens:
        device_tokens = [ut.device_token for ut in apns_user_tokens]
        app.logger.info("SEND TO: %s " % (device_tokens))
        config = app.config["apns"]
        if config.get("debug"):
            app.logger.info("APNS: UserID: %s - Devices: %s - Message: %s" % (ut.user_id, device_tokens, message))
            return

        job = high_queue.enqueue_call(
            func=apns.send,
            args=(device_tokens, ),
            kwargs={
                "alert": message
            },
            result_ttl=100,  # get result and delete immediately
        )

        app.logger.info("JOB ID: %s " % (job.get_id()))
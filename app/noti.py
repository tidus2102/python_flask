from flask import current_app as app
from app import apns, gcm
from app.models.user import User
from app.models.user_token import UserToken
from queue import high_queue

def sendNoti(type, user_id, message, optionData):
    from app.models.common import db1
    user = db1.session.query(User).get(user_id)

    user_tokens = None
    if type == 'apns':
        user_tokens = user.user_tokens.filter(
            UserToken.device_token != None,
            UserToken.device_type == UserToken.DEVICE_TYPE_APNS,
            UserToken.is_active == True
        ).all()
    if type == 'gcm':
        user_tokens = user.user_tokens.filter(
            UserToken.device_token != None,
            UserToken.device_type == UserToken.DEVICE_TYPE_GCM,
            UserToken.is_active == True
        ).all()

    if user_tokens:
        device_tokens = [user_token.device_token for user_token in user_tokens]
        app.logger.info("SEND NOTIFICATION TO: %s - %s " % (type, device_tokens))

        # config = app.config["apns"]
        # if config.get("debug"):
        #     app.logger.info("%s: UserID: %s - Devices: %s - Message: %s" % (type, ut.user_id, device_tokens, message))
        #     return

        if type == 'apns':
            # apns.send(device_tokens, alert = message, sound = 'default', data = optionData)

            job = high_queue.enqueue_call(
                func=apns.send,
                args=(device_tokens, ),
                kwargs={
                    "alert": message,
                    "sound": 'default',
                    "data": optionData
                },
                result_ttl=100,  # get result and delete immediately
            )

        if type == 'gcm':
            optionData['alert'] = message
            # gcm.send(device_tokens, data = optionData)

            job = high_queue.enqueue_call(
                func=gcm.send,
                args=(device_tokens, ),
                kwargs=optionData,
                result_ttl=100,  # get result and delete immediately
            )
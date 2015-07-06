from gcmclient import GCM, JSONMessage
from app import app


# def _do_send(message):
#     config = app.config["gcm"]
#     gcm = GCM(config["api_key"])
#
#     response = gcm.send(message)
#
#     # TODO: Update registration IDs (whatever that means)
#     for reg_id, new_reg_id in response.canonical.items():
#         app.logger.warning("GCM: Device: {0} => {1}".format(reg_id, new_reg_id))
#
#     # TODO: Invalid tokens, notify admin and disable them
#     for reg_id in response.not_registered:
#         app.logger.error("GCM: Device: {0} - invalid".format(reg_id))
#
#     # TODO: Handle other errors, notify admin
#     for reg_id, err_code in response.failed.items():
#         app.logger.error("GCM: Error: {0} - {1}".format(reg_id, err_code))
#
#     return response
#
#
# @inlineCallbacks
# def send(registration_ids, data, **options):
#     count, message = 0, JSONMessage(registration_ids, data, **options)
#
#     # TODO: Make max-retries configurable maybe
#     while count < 3:
#         response = yield deferToThread(_do_send, message)
#         if response.needs_retry():
#             count, message = count + 1, response.retry()
#             delay = response.delay(count)
#             response = None
#         else:
#             break
#
#     returnValue(response)

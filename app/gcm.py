from app import app
from gcmclient import *

def _do_send(tokens, **kwargs):
    config = app.config["gcm"]

    # Pass 'proxies' keyword argument, as described in 'requests' library if you
    # use proxies. Check other options too.
    # app.logger.info('==================')
    # app.logger.info(config["api_key"])
    gcm = GCM(config["api_key"])

    # Construct (key => scalar) payload. do not use nested structures.
    data = kwargs['data']
    # app.logger.info('==================')
    # app.logger.info(data)

    # Unicast or multicast message, read GCM manual about extra options.
    # It is probably a good idea to always use JSONMessage, even if you send
    # a notification to just 1 registration ID.
    #unicast = PlainTextMessage("registration_id", data, dry_run=True)
    #multicast = JSONMessage(tokens, data, collapse_key='news_publish', dry_run=True)
    multicast = JSONMessage(tokens, data)

    try:
        # attempt send
        # res_unicast = gcm.send(unicast)
        # res_multicast = gcm.send(multicast)
        res = gcm.send(multicast)

        # for res in [res_unicast, res_multicast]:
        # nothing to do on success
        for reg_id, msg_id in res.success.items():
            app.logger.info('==================')
            app.logger.info("Successfully sent %s as %s" % (reg_id, msg_id))

        # update your registration ID's
        for reg_id, new_reg_id in res.canonical.items():
            app.logger.info("Replacing %s with %s in database" % (reg_id, new_reg_id))

        # probably app was uninstalled
        for reg_id in res.not_registered:
            app.logger.info("Removing %s from database" % reg_id)

        # unrecoverably failed, these ID's will not be retried
        # consult GCM manual for all error codes
        for reg_id, err_code in res.failed.items():
            app.logger.info("Removing %s because %s" % (reg_id, err_code))

        # if some registration ID's have recoverably failed
        if res.needs_retry():
            # construct new message with only failed regids
            retry_msg = res.retry()
            # you have to wait before attemting again. delay()
            # will tell you how long to wait depending on your
            # current retry counter, starting from 0.
            app.logger.info("Wait or schedule task after %s seconds" % res.delay(1))
            # retry += 1 and send retry_msg again

    except GCMAuthenticationError:
        # stop and fix your settings
        app.logger.info("Your Google API key is rejected")
    except ValueError, e:
        # probably your extra options, such as time_to_live,
        # are invalid. Read error message for more info.
        app.logger.info("Invalid message/option or invalid GCM response")
        app.logger.info(e.args[0])
    except Exception:
        # your network is down or maybe proxy settings
        # are broken. when problem is resolved, you can
        # retry the whole message.
        app.logger.info("Something wrong with requests library")


def send(tokens, **kwargs):
    # TODO: Better to defer to a thread pool of size 1 (in the long
    # term we may switch to a job queue system like Celery, or
    # signaling a separate process dedicated to sending push
    # notifications).

    _do_send(tokens, **kwargs)

    # def run(tokens, **kwargs):
    #     _do_send(tokens, **kwargs)
    #
    # thread = threading.Thread(target=run, args=(tokens,), kwargs=kwargs)
    # thread.daemon = True
    # thread.start()
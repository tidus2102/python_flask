from apns_clerk import Session, APNs, Message

# TODO: Use feedback service to remove invalid tokens (need DB access
# from Twisted's threads (probably just create SQLAlchemy/Storm
# connections ourselves))

_session = Session()
_connection = None

def _get_connection():
    global _connection
    if _connection is None:
        from app import app
        config = app.config["apns"]
        _connection = _session.get_connection(
            "push_sandbox" if config.get("sandbox") else "push_production",
            cert_file=config.get("cert_file")
        )
    return _connection

def _do_send(tokens, **kwargs):
    from app import app
    message = Message(tokens, **kwargs)
    service = APNs(_get_connection())

    app.logger.info("_DO_SEND TO %s" % (tokens))
    while message:
        response = service.send(message)
        for token, reason in response.failed.items():
            code, errmsg = reason
            # TODO: Invalid tokens, notify admin and disable them
            app.logger.error("APNS: Device: %s - %s - %s" % (token, code, errmsg))

        # Failures not related to devices. TODO: notify admin
        for code, errmsg in response.errors:
            app.logger.error("APNS: Error: %s - %s" % (code, errmsg))

        # Check if there are tokens that can be retried
        if response.needs_retry():
            message = response.retry()
            app.logger.warning("APNS: retrying %s" % (message))
        else:
            message = None

    return response


def send(tokens, **kwargs):
    from app import app
    # TODO: Better to defer to a thread pool of size 1 (in the long
    # term we may switch to a job queue system like Celery, or
    # signaling a separate process dedicated to sending push
    # notifications).
    _do_send(tokens, **kwargs)

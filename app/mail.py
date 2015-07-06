import mandrill
from app import app
from app.utils import helper
from queue import low_queue


def _send(to_list, subject, content, sender_mail=None, sender_name=None, attachment=None,
         reply_to=None, bcc=None):

    config = app.config["email"]
    if config.get("debug"):
        app.logger.info("EMail: Subject: %s - To: %s - Message: %s" % (subject, to_list, content))
        return

    api_key = config["mandrill"]["api_key"]
    try:
        mandrill_client = mandrill.Mandrill(api_key)
        message = {
            # TODO: apply attachments
            # 'attachments': [{
            #     'content': 'ZXhhbXBsZSBmaWxl',
            #     'name': 'myfile.txt',
            #     'type': 'text/plain'
            # }],
            'bcc_address': bcc if bcc else None,
            'from_email': sender_mail if sender_mail else config.get("sender_mail"),
            'from_name': sender_name if sender_name else config.get("sender_name"),
            'headers': {
                'Reply-To': reply_to
            },
            'html': content,
            'subject': subject,
            'to': [{
                'email': to.get("email"),
                'name': helper.get(to, "name", None),
                'type': 'to'
            } for to in to_list],
            'track_clicks': True,
            'track_opens': True,
            'tracking_domain': True,
            'view_content_link': True
        }

        result = mandrill_client.messages.send(
            message=message,
            async=True,
        )

        app.logger.info("EMAIL RESULT: %s" % (result))

        '''
        [{'_id': 'abc123abc123abc123abc123abc123',
          'email': 'recipient.email@example.com',
          'reject_reason': 'hard-bounce',
          'status': 'sent'}]
        '''
    except mandrill.Error, e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
        raise


def send(to_list, subject, content, sender_mail=None, sender_name=None, attachment=None,
         reply_to=None, bcc=None):
    job = low_queue.enqueue_call(
        func=_send,
        args=(to_list, subject, content, sender_mail, sender_name, attachment, reply_to, bcc),
        result_ttl=5000,    # get result and delete immediately
    )
    app.logger.info("EMAIL JOB ID: %s " % (job.get_id()))
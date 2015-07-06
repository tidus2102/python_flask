from app import app, job
from flask.ext.script import Manager

manager = Manager(app)
#manager.add_command('check_expired', job.CheckExpired())
#manager.add_command('notify_expired', job.NotifyExpired())

@manager.command
def hashAccessToken():
    from app.models.user_token import UserToken
    from app.models import db
    import bcrypt

    user_tokens = UserToken.query.all()
    for ut in user_tokens:
        print "ID: %s AT: %s" % (ut.id, ut.access_token)
        ut.access_token = bcrypt.hashpw(ut.access_token, bcrypt.gensalt(10))
        print "ID: %s AT: %s" % (ut.id, ut.access_token)
        db.session.add(ut)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
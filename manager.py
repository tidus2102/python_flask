from app import app
from flask.ext.script import Manager
#from app.command import job

manager = Manager(app)
#manager.add_command('check_expired', job.CheckExpired())
#manager.add_command('notify_expired', job.NotifyExpired())

if __name__ == "__main__":
    manager.run()
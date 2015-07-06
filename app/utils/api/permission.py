from functools import wraps
from app.models.bag import Bag
from app.models.user import User
from flask.ext.restful import abort
from flask.ext.babelex import gettext

#
# def checkPatyPermission(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         pid = kwargs.get("pid")
#         user = kwargs.get("user")
#         paty = Paty.findById(pid)
#
#         if not paty:
#             abort(404, message=gettext("NOT_FOUND"))
#
#         if not paty.checkPermission(user.id):
#             abort(403, message=gettext("PERMISSION_DENIE"))
#
#         return f(*args, **kwargs)
#     return decorator
#
#
# def checkVotePermission(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         tvId = kwargs.get("tvId")
#         user = kwargs.get("user")
#
#         time_vote = TimeVote.findById(tvId)
#
#         if not time_vote:
#             abort(404, message=gettext("NOT_FOUND_VOTING"))
#
#         paty = time_vote.paty
#
#         if not paty:
#             abort(404, message=gettext("NOT_FOUND_PATY"))
#
#         if not paty.checkPermission(user.id):
#             abort(403, message=gettext("PERMISSION_DENIE"))
#
#         return f(*args, **kwargs)
#     return decorator
#
#
# def checkPatyCreator(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         pid = kwargs.get("pid")
#         user = kwargs.get("user")
#         paty = Paty.findById(pid)
#
#         if not paty:
#             abort(404, message=gettext("NOT_FOUND"))
#
#         if not paty.isCreator(user.id):
#             abort(403, message=gettext("PERMISSION_DENIE"))
#
#         return f(*args, **kwargs)
#     return decorator
#
#
# def checkAccessUserResource(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         friend_id = kwargs.get("uid")
#         logged_user = kwargs.get("user")
#         friend_user = User.findById(friend_id)
#         if not friend_user:
#             abort(404, message=gettext("NOT_FOUND"))
#
#         # Himself so pass
#         if logged_user.id == friend_user.id:
#             return f(*args, **kwargs)
#
#         # Just friend can see each other
#         if not friend_user.isFriendWith(logged_user.id):
#             abort(403, message=gettext("PERMISSION_DENIE"))
#
#         return f(*args, **kwargs)
#     return decorator
#
#
# def checkPatyToken(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = kwargs.get("token")
#
#         if not token:
#             abort(404, message=gettext("NOT_FOUND"))
#
#         paty = Paty.findByAttributes(token=token)
#         if not paty:
#             abort(404, message=gettext("NOT_FOUND"))
#
#         kwargs['paty'] = paty
#
#         return f(*args, **kwargs)
#     return decorator
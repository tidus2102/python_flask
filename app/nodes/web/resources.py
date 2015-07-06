from flask import Blueprint, redirect, abort
from flask import request
from app.utils import helper
from app.models.user import User
from app.models.photo import Photo
from app.cache import cache

resources = Blueprint('resources', __name__)

@resources.route('/resources/user/<user_id>/avatar', methods=('GET', ))
def user_avatar(user_id):
    type = helper.get(request.args, "type", "origin")
    if not type in ["origin", "thumb", "small"]:
        type = "origin"

    user = User.findById(user_id)
    if user:
        return redirect(user.getAvatar(type))

    return "Avatar Not Found"

@resources.route('/resources/photo/<photo_id>', methods=('GET', ))
def photo(photo_id):
    type = helper.get(request.args, "type", "origin")
    if not type in ["origin", "thumb", "small"]:
        type = "origin"

    photo = Photo.findById(photo_id)
    if photo:
        return redirect(photo.getPhotoUrl(type))

    return "Photo Not Found"

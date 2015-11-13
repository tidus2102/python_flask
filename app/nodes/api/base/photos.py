from flask.ext.babelex import gettext
from app.utils.api import ApiResource
from app.utils.api.authentication import authenticate
from app.models.photo import Photo
from app.models.common import db
from flask.ext.restful import reqparse, abort
from werkzeug.datastructures import FileStorage


class ApiPhotoList(ApiResource):
    """
    Handle the the api with endpoint: /photos
    """
    def __init__(self):
        # Validation rules for post method
        self.postParser = reqparse.RequestParser()
        self.postParser.add_argument(
            "image", required=True, type=FileStorage, location='files',
            help=gettext("%(field)s VALIDATION_REQUIRED_ERROR", field="image"))


    @authenticate(need_auth=True)
    def post(self, user):
        """
        Submit new photo
        Params:
            user: the User instance that pass authentication (logged user)

        Request params:
            image: file,

        Response:
        {
            "id": 111,
        }
        """
        data = self.postParser.parse_args()

        # Update photo
        photo = Photo.create(user.id)
        photo.updateImage(data["image"])

        # Commit query and write to db
        db.session.commit()

        return photo.format_json()


class ApiPhoto(ApiResource):
    """
    Handle the the api with endpoint: /photos/<pid>
    """
    def __init__(self):
        pass


    @authenticate(need_auth=True)
    def delete(self, pid, user):
        """
        Delete photo
        Params:
            user: the User instance that pass authentication (logged user)

        Request params:

        Response:
        {
            "id": 111,
        }
        """
        # Update photo
        photo = Photo.findById(pid)
        if not photo:
            abort(404, message=gettext("NOT_FOUND"))

        if photo.isOwner(user.id):
            abort(403, message=gettext("PERMISSION_DENIE"))

        # Commit query and write to db
        db.session.delete(photo)
        db.session.commit()
        return {"id": pid}

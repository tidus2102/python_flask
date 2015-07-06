from app.nodes.api.base.photos import ApiPhotoList as _ApiPhotoList, ApiPhoto as _ApiPhoto


class ApiPhotoList(_ApiPhotoList):
    """
    Handle the the api with endpoint: /photos
    """
    pass


class ApiPhoto(_ApiPhoto):
    """
    Handle the the api with endpoint: /photos/<pid>
    """
    pass

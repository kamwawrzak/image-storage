class DetailedException(Exception):

    def __init__(self, detail: str):
        self.detail = detail

class ValidationError(DetailedException):
    pass

class AuthenticationError(DetailedException):
    pass

class UploadImageError(DetailedException):
    pass

class GetImageError(DetailedException):
    pass

class S3ClientError(DetailedException):
    pass

class RecordAlreadyExistsError(DetailedException):
    pass

class NotFoundError(Exception):
    pass

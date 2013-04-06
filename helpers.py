from flask import session
from werkzeug.routing import BaseConverter, ValidationError
from base64 import b64encode, b64decode
from bson.objectid import ObjectId
from bson.errors import InvalidId
from functools import wraps


def authorized():
    def wrapper(a):
        @wraps(a)
        def wrapped(*args, **kwargs):
            if session['signed_in'] != True:
                return 'error!'
            return a(*args, **kwargs)
        return wrapped
    return wrapper


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(b64decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return b64encode(value.binary)

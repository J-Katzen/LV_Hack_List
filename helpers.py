from flask import session, request
from werkzeug.routing import BaseConverter, ValidationError
from base64 import b64encode, b64decode
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from bson.errors import InvalidId
from functools import wraps
import urllib2



def authorized(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'signed_in' not in session:
            return 'Not signed in!'
        return f(*args, **kwargs)
    return wrapped


def parse_amz(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    image_url = soup.select("#main-image")[0]['src']
    name = soup.select("#btAsinTitle")[0].text
    descript = soup.select(".productDescriptionWrapper")[0].text[:160] + "..."
    obj = {'name': name, 'image_url': image_url, 'description': descript}
    return obj


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(b64decode(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return b64encode(value.binary)

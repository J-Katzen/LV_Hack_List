# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~

    Settings file for our little demo.

    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.

    :copyright: (c) 2012 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os

# We want to seamlessy run our API both locally and on Heroku so:
if os.environ.get('PORT'):
    # We're hosted on Heroku!  Use the MongoHQ sandbox as our backend.
    MONGO_HOST = 'alex.mongohq.com'
    MONGO_PORT = 10047
    MONGO_USERNAME = 'evedemo'
    MONGO_PASSWORD = 'evedemo'
    MONGO_DBNAME = 'app9346575'

    # also, correctly set the API entry point
    SERVER_NAME = 'eve-demo.herokuapp.com'
else:
    # Running on local machine. Let's just use the local mongod instance.
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'user'
    MONGO_DBNAME = 'apitest'

    # let's not forget the API entry point
    SERVER_NAME = 'localhost:5000'


# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'users': people,
    'lists': lists,
}

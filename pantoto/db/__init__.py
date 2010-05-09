from django.conf import settings
from pymongo import Connection
import pymongo.errors

OperationFailure = pymongo.errors.OperationFailure
_connection = Connection(settings.MONGODB_HOST, settings.MONGODB_PORT)
database = _connection[settings.MONGODB_NAME] if _connection else None


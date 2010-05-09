# Threadlocals middleware to make available current_user anywhere

from django.conf import settings
from pantoto.auth import User
import os
try:
    import cPickle as pickle
except:
    import pickle

def get_current_uid():
    user_obj = os.path.join(settings.DB_DIR,'session_user.obj')
    if os.path.exists(user_obj):
        user_obj = open(os.path.join(settings.DB_DIR,'session_user.obj'),'r')
        uid = pickle.load(user_obj)
        user_obj.close()
        return uid
    else:
        return None

class ThreadLocals(object):

    """Middleware that gets various objects from the

    request object and saves them in thread local storage."""

    def process_request(self, request):
        user = getattr(request,'user', None)
        if not user.is_anonymous():
            uid = user.get_id()
            user_obj = os.path.join(settings.DB_DIR,'session_user.obj')
            if os.path.exists(user_obj):
                os.remove(user_obj)
            user_obj = open(user_obj,'wb')
            pickle.dump(uid,user_obj)
            user_obj.close()
        return


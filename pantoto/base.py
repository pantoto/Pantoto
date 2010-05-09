
class PanObj(object):

    objects = None
    list_fields = []
    valid_fields = ('id',)
    _id_prefix = "o"
    messages = []

    def __init__(self, result):
        self._fields = result

    def __getattr__(self, attr):
        try:
            return self._fields[attr]
        except KeyError:
            return None

    def __setattr__(self, attr, value):
        if attr in ['id', '_fields']:
            object.__setattr__(self, attr, value)
        else:
            self._fields[attr] = value

    def save(self):
        if not self._fields.get('id',None):
            self._fields['id'] = self._id_prefix + str(self.objects.find().count() + 1)
        self._fields['_id'] = self.objects.save(self._fields, safe=True)
        
    def delete(self):
        self.objects.remove({'_id': self._fields.get('_id', None)})

    def set(self, fields, safe=False):
        self.objects.update({'_id':self.id}, {'$set': fields}, safe=safe)
        self._fields = self.objects.find_one({'_id':self.id})

    def getauthors(self):
        return self.authors

    #Added to retrieve the generated ID and not the Mongo Object ID
    def get_id(self):
        id = 0
        obj=self.objects.find_one({'_id':self._id})
        id = obj['id']
        return id

    def get_doc(self):
        return self._fields

    def __unicode__(self):
        return ''

    id = property(get_id)
    doc = property(get_doc)

    @classmethod
    def get(cls, spec):
        if cls.objects:
            result = cls.objects.find_one(spec)
            if result:
                return cls(result)
        return None

    @classmethod
    def create(cls,data):
        obj = cls(data)
        obj.save()
        return obj

    @classmethod
    def all(cls,lst=False):
        if not lst:
            return list(cls.objects.find())
        ret_lst = []
        for obj in cls.objects.find():
            row = []
            for field in cls.list_fields:
                row.append(obj[field])
            row.append(obj['id'])
            ret_lst.append(row)
        return ret_lst

    @classmethod
    def all_by_criteria(cls,criteria,lst=False):
        if not lst:
            return list(cls.objects.find(criteria))
        ret_lst = []
        for json in cls.objects.find(criteria):
            obj = cls(json)            
            ret_lst.append(obj)
        return ret_lst


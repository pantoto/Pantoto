from pantoto.db import database as db
from pantoto.middleware.threadlocals import get_current_uid
from django import forms
from pantoto.utils import *
from pantoto.base import PanObj
from pantoto.auth import User

MERGE_RULES =\
{'rwrw':'rw','r-r-':'r-','w-w-':'w-','rwr-':'rw','r-rw':'rw','rww-':'rw','w-rw':'rw','r-w-':'rw','w-r-':'rw','rnnw':'rw','rnrn':'rw','nwrn':'rw','nwnw':'rw'}

class Field(PanObj):

    objects = db.fields
    list_fields = ['id','label','type','required']
    valid_fields =\
    ('id','label','type','required','initial','choices','rows','cols','choices','max_length','help_text')
    _id_prefix = "f"
    messages = []

    @classmethod
    def for_choices(cls):
        choices = []
        for field in cls.all():
            choices.append((field['id'],field['label']))
        return choices

    def get_choices(self):
        return [ (choice,choice) for choice in self.choices.strip().split('|') ]

class View(PanObj):

    objects = db.views
    list_fields = ['id','name']
    valid_fields = ('id','name','fal')
    _id_prefix = "v"
    messages = []
    
    @classmethod
    def for_choices(cls):
        choices = []
        for view in cls.all():
            choices.append((view['id'],view['name']))
        return choices

class Pagelet(PanObj):

    objects = db.pagelets
    list_fields = ['id','name','draft']
    valid_fields = ('id','name','description','draft','fields')
    _id_prefix = "p"

    def _merge_fal(self):
        mv = {}
        for view_id in self.views:
            view = View.get({'id':view_id})
            for fid,perms in view.fal.items(): 
                if mv.has_key(fid):
                    for perm_id,perm in perms.items():
                        if perm_id in mv[fid].keys():
                            mvperms = mv[fid]
                            mvperms[perm_id] = MERGE_RULES[perm+mvperms[perm_id]]
                            mv[fid] = mvperms
                        else:
                            mv[fid].update({perm_id:perm})
                else:
                    mv.update({fid:perms})
        return mv

    def _make_field(self,fid,perm):
        READONLY_PERMS = ('r-','-w',)
        deco = Field.get({'id':fid})
        initial = deco.initial
        if deco.type == "textarea":
            field = forms.CharField(initial=initial,widget=forms.Textarea(attrs={'rows':deco.rows,'cols':deco.cols}))
        elif deco.type == "dropdown":
            field = forms.ChoiceField(initial=initial,choices=deco.get_choices())
        elif deco.type == "dropdownmul":
            field = forms.MultipleChoiceField(initial=initial,choices=deco.get_choices())
        elif deco.type == "checkbox":
            field = forms.MultipleChoiceField(initial=initial,choices=deco.get_choices(),widget=forms.CheckboxInput())
        elif deco.type == "radio":
            field = forms.MultipleChoiceField(initial=initial,choices=deco.get_choices(),widget=forms.RadioSelect())
        elif deco.type == "date":
            field = forms.DateField()
        elif deco.type == "time":
            field = forms.TimeField()
        elif deco.type == "datetime":
            field = forms.DateTimeField()
        elif deco.type == "email":
            field = forms.EmailField()
        elif deco.type == "integer":
            field = forms.IntegerField()
        elif deco.type == "float":
            field = forms.FloatField()
        elif deco.type == "url":
            field = forms.URLField()
        elif deco.type == "file":
            field = forms.FileField()
        else:
            field = forms.CharField(max_length=deco.max_length,initial=deco.initial)
        if perm in READONLY_PERMS:
            field.required = False
            label = underscorify(deco.label)+"*"
        else:
            field.required = True
            label = underscorify(deco.label)
        field.label = deco.label
        return {label:field}

    def _make_form(self,fields):
        return type('PageletForm', (forms.BaseForm,), { 'base_fields': fields })

    def get_fields(self):
        mv = self._merge_fal()
        return mv.keys()

    def save_post(self,data):
        self.post = {}
        for fid in self.get_fields():
            field = Field.get({'id':fid})
            field_name = underscorify(field.label)
            if data.has_key(field_name):
                self.post.update({fid:data[field_name]})
        self.save()
        return

    def get_post(self):
        post = {}
        for fid in self.get_fields():
            field = Field.get({'id':fid})
            field_name = underscorify(field.label)
            if self.post.has_key(fid):
                post.update({field_name:self.post[fid]})
        return post
            
    def get_form(self):
        mv = self._merge_fal()
        user = User.get({'id':get_current_uid()})
        fields = {'name':forms.CharField(label='Name',max_length=255,initial=self.name),'description':forms.CharField(label='Description',widget=forms.Textarea(),initial=self.description)}
        for fid,perm in mv.items():
            for persona in user.get_personas():
                if perm.has_key(persona):
                    fields.update(self._make_field(fid,perm[persona]))
        PageletForm = self._make_form(fields)
        if self.post:
            form = PageletForm(initial=self.get_post())
        else:
            form = PageletForm()
        return form

class Site(PanObj):
    
    objects = db.sites
    list_fields = ['id','name','description','category','theme']
    valid_fields = ('id','name','description','category','theme')
    _id_prefix = "s"
    messages = []

    @classmethod
    def all(cls,lst=True):
        sites = super(Site,cls).all(lst)
        if lst:
            for site in sites:
                category_id = site[3]
                category = Category.get({"id":category_id})
                site[3] = category.name
                theme_file = site[4]
                site[4] = lookup_tuple(THEME_TYPES,theme_file)
        return sites

class Category(PanObj):

    objects = db.categories
    list_fields = ['id','name','description','parent']
    valid_fields = ('id','name','description','parent')
    _id_prefix = "c"
    messages = []

    @classmethod
    def for_choices(cls,selfref=False):
        choices = [] 
        if selfref:
            choices.append(("none","Top Level"))
        for category in cls.all(lst=False):
            choices.append((category['id'],category['name']))
        return choices

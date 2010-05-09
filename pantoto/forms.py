from django import forms 
from pantoto.auth import User,Persona
from pantoto.models import Field,View,Pagelet,Category,Site
from pantoto.utils import *

FIELD_TYPES = (
    ('text','Text'),
    ('textarea', 'Paragraph'),
    ('dropdown','Drop Down'),
    ('dropdownmul','Drop Down Multiple'),
    ('checkbox','Check Box'),
    ('radio','Radio'),
    ('date','Date'),
    ('time','Time'),
    ('datetime','Date Time'),
    ('email','Email'),
    ('integer','Integer'),
    ('float','Float'),
    ('url','URL'),
    ('file','File')
)

class UserForm(forms.Form):
    username         = forms.CharField(max_length=255)
    first_name       = forms.CharField(max_length=255)
    last_name        = forms.CharField(max_length=255)
    email            = forms.EmailField()
    password         = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    is_active        = forms.BooleanField(required=False,initial=True)

    def clean_password(self):
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean_username(self):
        if User.get({'username':self.data['username']}):
            raise forms.ValidationError('Username already exists')
        return self.data['username']
        
    def clean(self,*args, **kwargs):
        self.clean_password()
        self.clean_username()
        return super(UserForm, self).clean(*args, **kwargs)

class EditUserForm(forms.Form):
    username         = forms.CharField(max_length=255)
    first_name       = forms.CharField(max_length=255)
    last_name        = forms.CharField(max_length=255)
    email            = forms.EmailField()
    is_active        = forms.BooleanField(required=False,initial=True)

    def for_instance(self,instance):
        for field in self.base_fields.keys():
            if instance.has_key(field):
                self.base_fields[field].initial = instance[field]

class ChangePasswordForm(forms.Form):
    password         = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value=False))

    def clean_password(self):
        if self.data['password'] != self.data['confirm_password']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self,*args, **kwargs):
       return super(ChangePasswordForm, self).clean(*args, **kwargs)

class PersonaForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    users = forms.MultipleChoiceField(choices=User.for_choices(),required=False)

class FieldForm(forms.Form):
    label = forms.CharField(max_length=255)
    field_type = forms.CharField(max_length = 255,widget=forms.Select(choices = FIELD_TYPES))
    required = forms.BooleanField(required=False)
    help_text = forms.CharField(max_length=255,required=False)
    initial = forms.CharField(max_length=255,help_text="Multiple Values seperated by '|' For Checkbox and Multiple Select")
    choices = forms.CharField(max_length=255,widget=forms.Textarea(),help_text="Enter\
                choices seperated by '|'.Eg: Apple | Orange | Strawberries")
    max_length = forms.IntegerField(required=False)
    rows = forms.IntegerField(required=False)
    cols = forms.IntegerField(required=False)

class ViewForm(forms.Form):
    name = forms.CharField(max_length=255)
    fields = forms.MultipleChoiceField(choices=Field.for_choices())

class PageletForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':15,'cols':80}))
    views = forms.MultipleChoiceField(choices=View.for_choices())
    draft = forms.BooleanField(required=False)

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea())
    parent = forms.CharField(max_length = 255,widget=forms.Select(choices = Category.for_choices(True)))

class SiteForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    category = forms.CharField(max_length = 255,widget=forms.Select(choices = Category.for_choices()))
    theme = forms.CharField(max_length = 255,widget=forms.Select(choices = THEME_TYPES))


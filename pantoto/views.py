from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.template import RequestContext
from django.conf import settings
from django.utils import simplejson
from pantoto.auth import User,Persona
from pantoto.models import *
from pantoto.forms import *
from pantoto.utils import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate,login,logout
import os
 
def do_login(request):
    if request.method == "POST":
        next = request.POST['next']
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if not user:
            errors = 'Invalid Username or Password'
        else:
            login(request,user)
            return HttpResponseRedirect(next) 
    else:
        errors = ""
        next = request.GET.get('next','/')
    return render_to_response('pantoto/login.html',{'errors':errors,'next':next})

def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def do_change_password(request):
    if request.method == "POST":
       form = ChangePasswordForm(request.POST)
       if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.messages.append('Successfully changed password ')
            return HttpResponseRedirect('/user/')
    else:
        form = ChangePasswordForm()
    return render_to_response('pantoto/add_obj.html',{'form':form,'obj':'Password'})

def get_help(request):
    obj_type = request.GET['type']
    helptext = get_helptext(obj_type)
    return render_to_response('pantoto/help.html',{'helptext':helptext})

def do_index(request):
    return render_to_response('pantoto/index.html',{},context_instance=RequestContext(request))

#Handling pagination from within django
def paged_listing(request, obj_list):

    paginator = Paginator(obj_list, 5) # Limit set to 5 per page
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        objs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objs = paginator.page(paginator.num_pages)
    return objs

def list_users(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'user','objs':paged_listing(request, User.all(lst=True)) \
                ,'fields':User.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_user(request):
    if request.method == "POST":
       form = UserForm(request.POST)
       if form.is_valid():
            user = User.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = form.cleaned_data['is_active']
            user.save()
            request.user.messages.append('Successfully added user ' + user.username)
            return HttpResponseRedirect('/user/')
    else:
        form = UserForm()
    return render_to_response('pantoto/add_obj.html',{'form':form,'add':True})

@login_required
def edit_user(request,user_id):
    user = User.get({'id':user_id})
    if not user:
        raise Http404('User Does Not Exist')
    if request.method == "POST":
        form = EditUserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = form.cleaned_data['is_active']
            user.email = form.cleaned_data['email']
            user.save()
            request.user.messages.append('Successfully updated user ' + user.username)
            return HttpResponseRedirect('/user/')
    else:
        form = EditUserForm(initial={'username':user.username,'first_name':user.first_name,'last_name':user.last_name,'email':user.email,'is_active':user.is_active})
        return render_to_response('pantoto/add_obj.html',{'form':form,'add':False,'obj':'User'})

@login_required
def delete_user(request,user_id):
    user = User.get({'id':user_id})
    if not user:
        raise Http404('User Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted user ' + user.username)
        user.delete()
        return HttpResponseRedirect('/user/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'User'})
  
@login_required
def list_personas(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'persona','objs':paged_listing(request,Persona.all(lst=True)) \
            ,'fields':Persona.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_persona(request):
    if request.method == "POST":
       form = PersonaForm(request.POST)
       if form.is_valid():
            persona = Persona.create({'name':form.cleaned_data['name'],'description':form.cleaned_data['description'],'users':form.cleaned_data['users']})
            request.user.messages.append('Successfully added persona ' + persona.name)
            return HttpResponseRedirect('/persona/')
    else:
        form = PersonaForm()
    return render_to_response('pantoto/add_obj.html',{'form':form,'add':True,'obj':'Persona'})

@login_required
def edit_persona(request,persona_id):
    persona = Persona.get({'id':persona_id})
    if not persona:
        raise Http404('Persona Does Not Exist')
    if request.method == "POST":
        form = PersonaForm(request.POST)
        if form.is_valid():
            persona.name = form.cleaned_data['name']
            persona.description = form.cleaned_data['description']
            persona.users = form.cleaned_data['users']
            persona.save()
            request.user.messages.append('Successfully updated persona ' + persona.name)
            return HttpResponseRedirect('/persona/')
    else:
        form = PersonaForm(initial={'name':persona.name,'description':persona.description,'users':persona.users})
        return render_to_response('pantoto/add_obj.html',{'form':form,'add':False})

@login_required
def delete_persona(request,persona_id):
    persona = Persona.get({'id':persona_id})
    if not persona:
        raise Http404('Persona Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted persona ' + persona.name)
        persona.delete()
        return HttpResponseRedirect('/persona/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'Persona'})

@login_required
def list_fields(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'field','objs':paged_listing(request, Field.all(lst=True)),\
            'fields':Field.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_field(request):
    if request.method == "POST":
       form = FieldForm(request.POST)
       if form.is_valid():
            field = Field.create({'label':form.cleaned_data['label'],'type':form.cleaned_data['field_type'],'required':form.cleaned_data['required']})
            request.user.messages.append('Successfully added field ' + field.label)
            return HttpResponseRedirect('/field/')
    else:
        form = FieldForm()
    return render_to_response('pantoto/add_field.html',{'form':form,'add':True})

@login_required
def edit_field(request,field_id):
    field = Field.get({'id':field_id})
    if not field:
        raise Http404('Field Does Not Exist')
    if request.method == "POST":
        form = FieldForm(request.POST)
        if form.is_valid():
            field.label = form.cleaned_data['label']
            field.type = form.cleaned_data['type']
            field.required = form.cleaned_data['required']
            field.save()
            request.user.messages.append('Successfully updated field ' + field.label)
            return HttpResponseRedirect('/field/')
    else:
        form = FieldForm(initial={'label':field.label,'type':field.type,'required':field.required})
        return render_to_response('pantoto/add_field.html',{'form':form,'add':False})

@login_required
def delete_field(request,field_id):
    field = Field.get({'id':field_id})
    if not field:
        raise Http404('Field Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted field ' + field.label)
        field.delete()
        return HttpResponseRedirect('/field/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'Field'})

@login_required
def list_views(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'view','objs':paged_listing(request,View.all(lst=True)), \
            'fields':View.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_view(request):
    if request.method == "POST":
        fal = simplejson.loads(request.POST.get('fal','{}'))
        view = View.create({'name':request.POST['name'],'fields':request.POST.getlist('fields'),'fal':fal})
        request.user.messages.append('Successfully added View ' + view.name)
        return HttpResponse(simplejson.dumps({'success':True}),mimetype="application/javascript")
    else:
        return render_to_response('pantoto/add_view.html',{'add':True,'form':ViewForm(),'fields':Field.for_choices(),'personas':Persona.for_choices(),\
                                                            'permissions':PERMISSIONS},context_instance=RequestContext(request))

@login_required
def edit_view(request,view_id):
    view = View.get({'id':view_id})
    if request.method == "POST":
        fal = simplejson.loads(request.POST.get('fal','{}'))
        view.name = request.POST['name']
        view.fields = request.POST['fields']
        view.fal = fal
        view.save()
        request.user.messages.append('Successfully updated View ' + view.name)
        return HttpResponse(simplejson.dumps({'success':True}),mimetype="application/javascript")
    else:
        form = ViewForm(initial={'name':view.name,'fields':view.fields})
        return render_to_response('pantoto/add_view.html',{'add':False,'vid':view_id,'form':form,'permissions':PERMISSIONS,'personas':Persona.for_choices()})

@login_required
def get_view_fal(request,view_id):
    view = View.get({'id':view_id})
    fal = view.fal
    field_map = {}
    persona_map = {}
    for fid,perms in fal.items():
        field_map[fid] = Field.get({'id':fid}).label
        for pid in perms.keys():
            if not persona_map.has_key(pid):
                persona_map[pid] = Persona.get({'id':pid}).name
    return HttpResponse(simplejson.dumps({'fal':fal,'field_map':field_map,'persona_map':persona_map}),mimetype="application/javascript")

@login_required
def delete_view(request,view_id):
    view = View.get({'id':view_id})
    if not view:
        raise Http404('View Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted view ' + view.name)
        view.delete()
        return HttpResponseRedirect('/view/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'View'})

@login_required
def list_pagelet(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'pagelet','objs':paged_listing(request,Pagelet.all(lst=True)),'fields':Pagelet.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_pagelet(request):
    if request.method == "POST":
       form = PageletForm(request.POST)
       if form.is_valid():
            pagelet = Pagelet.create({'name':form.cleaned_data['name'],'views':form.cleaned_data['views'],'description':form.cleaned_data['description'],'draft':form.cleaned_data['draft']})
            request.user.messages.append('Successfully added pagelet ' + pagelet.name)
            return HttpResponseRedirect('/pagelet/')
    else:
       form = PageletForm()
    return render_to_response('pantoto/add_pagelet.html',{'form':form,'add':True,'obj':'Pagelet'})

@login_required
def delete_pagelet(request,pagelet_id):
    pagelet = Pagelet.get({'id':pagelet_id})
    if not pagelet:
        raise Http404('Persona Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted pagelet ' + pagelet.name)
        pagelet.delete()
        return HttpResponseRedirect('/pagelet/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'Pagelet'})
        
@login_required
def post_pagelet(request,pagelet_id):
    pagelet = Pagelet.get({'id':pagelet_id})
    if not pagelet:
        raise Http404('Pagelet Does Not Exist')
    if request.method == "POST":
        if pagelet.draft:
            pagelet = Pagelet.create({'name':request.POST['name'],'description':request.POST['description'],'views':pagelet.views,'draft':False})
        pagelet.save_post(request.POST)
        request.user.messages.append('Successfully posted pagelet ' + pagelet.name)
        return HttpResponseRedirect('/pagelet/')
    else:
        return render_to_response('pantoto/post_pagelet.html',{'form':pagelet.get_form()})

@login_required
def edit_pagelet(request,pagelet_id):
    pagelet = Pagelet.get({'id':pagelet_id})
    if not pagelet:
        raise Http404('Pagelet Does Not Exist')
    if request.method == "POST":
        form = PageletForm(request.POST)
        if form.is_valid():
            pagelet.name = form.cleaned_data['name']
            pagelet.views = form.cleaned_data['views']
            pagelet.description = form.cleaned_data['description']
            pagelet.draft = form.cleaned_data['draft']
            pagelet.save()
            request.user.messages.append('Successfully updated pagelet ' + pagelet.name)
            return HttpResponseRedirect('/pagelet/')
    else:
        form = PageletForm(initial={'name':pagelet.name,'views':pagelet.views,'description':pagelet.description,'draft':pagelet.draft})
    return render_to_response('pantoto/add_pagelet.html',{'form':form,'add':False})
        

@login_required
def list_categories(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'category','objs':paged_listing(request, Category.all(lst=True)),\
            'fields':Category.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_category(request):
    if request.method == "POST":
       form = CategoryForm(request.POST)
       if form.is_valid():
            category = Category.create({'name':form.cleaned_data['name'],'description':form.cleaned_data['description'],'parent':form.cleaned_data['parent']})
            request.user.messages.append('Successfully added category ' + category.name)
            return HttpResponseRedirect('/category/')
    else:
        form = CategoryForm()
    return render_to_response('pantoto/add_obj.html',{'form':form,'add':True,'obj':'Category'})

@login_required
def edit_category(request,category_id):
    category = Category.get({'id':category_id})
    if not category:
        raise Http404('Category Does Not Exist')
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            category.description = form.cleaned_data['description']
            category.parent = form.cleaned_data['parent']
            category.save()
            request.user.messages.append('Successfully updated category ' + category.name)
            return HttpResponseRedirect('/category/')
    else:
        form = CategoryForm(initial={'name':category.name,'description':category.description,'parent':category.parent})
        return render_to_response('pantoto/add_obj.html',{'form':form,'add':False})

@login_required
def delete_category(request,category_id):
    category = Category.get({'id':category_id})
    if not category:
        raise Http404('Category Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted category ' + category.name)
        category.delete()
        return HttpResponseRedirect('/category/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'category'})


@login_required
def list_sites(request):
    return render_to_response('pantoto/list_objs.html',{'klass':'site','objs':paged_listing(request, Site.all(lst=True)),\
            'fields':Site.list_fields},context_instance=RequestContext(request)) 

@login_required
def add_site(request):
    if request.method == "POST":
       form = SiteForm(request.POST)
       if form.is_valid():
            site = Site.create({'name':form.cleaned_data['name'],'description':form.cleaned_data['description'],\
                    'category':form.cleaned_data['category'],'theme':form.cleaned_data['theme']})
            request.user.messages.append('Successfully added site ' + site.name)
            return HttpResponseRedirect('/site/')
    else:
        form = SiteForm()
    return render_to_response('pantoto/add_obj.html',{'form':form,'add':True,'obj':'Site'})

@login_required
def edit_site(request,site_id):
    site = Site.get({'id':site_id})
    if not site:
        raise Http404('Site Does Not Exist')
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site.name = form.cleaned_data['name']
            site.description = form.cleaned_data['description']
            site.category = form.cleaned_data['category']
            site.theme = form.cleaned_data['theme']
            site.save()
            request.user.messages.append('Successfully updated site ' + site.name)
            return HttpResponseRedirect('/site/')
    else:
        form = SiteForm(initial={'name':site.name,'description':site.description,'category':site.category,'theme':site.theme})
        return render_to_response('pantoto/add_obj.html',{'form':form,'add':False})

@login_required
def delete_site(request,site_id):
    site = Site.get({'id':site_id})
    if not site:
        raise Http404('Site Does Not Exist')
    if request.method == "POST":
        request.user.messages.append('Successfully deleted site ' + site.name)
        site.delete()
        return HttpResponseRedirect('/site/')
    else:
        return render_to_response('pantoto/delete_obj.html',{'obj':'site'})

@login_required
def view_site(request,site_id):
    site = Site.get({'id':site_id})
    if not site:
        raise Http404('Site Does Not Exist')
    else:
        categories = Category.all_by_criteria({"parent":site.category})
        return render_to_response('pantoto/view_site.html',{'categories':categories,'site':site}) 

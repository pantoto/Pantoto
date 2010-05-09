from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',

    #comment out for production
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),

    ('^$','pantoto.views.do_index'),

    ('^login/$','pantoto.views.do_login'),

    ('^logout/$','pantoto.views.do_logout'),

    ('^change_password/$','pantoto.views.do_change_password'),

    (r'^user/$', 'pantoto.views.list_users'),

    (r'^user/add/$', 'pantoto.views.add_user'),

    (r'^user/(?P<user_id>\w+)/$', 'pantoto.views.edit_user'),

    (r'^user/(?P<user_id>\w+)/delete/$', 'pantoto.views.delete_user'),

    (r'^persona/$', 'pantoto.views.list_personas'),

    (r'^persona/add/$', 'pantoto.views.add_persona'),

    (r'^persona/(?P<persona_id>\w+)/$', 'pantoto.views.edit_persona'),

    (r'^persona/(?P<persona_id>\w+)/delete/$', 'pantoto.views.delete_persona'),

    (r'^field/$', 'pantoto.views.list_fields'),

    (r'^field/add/$', 'pantoto.views.add_field'),

    (r'^field/(?P<field_id>\w+)/$', 'pantoto.views.edit_field'),

    (r'^field/(?P<field_id>\w+)/delete/$', 'pantoto.views.delete_field'),

    (r'^pagelet/add/$', 'pantoto.views.add_pagelet'),
    
    (r'^pagelet/(?P<pagelet_id>\w+)/delete/$', 'pantoto.views.delete_pagelet'),

    (r'^pagelet/(?P<pagelet_id>\w+)/properties/$',\
                'pantoto.views.edit_pagelet'),
    
    (r'^pagelet/(?P<pagelet_id>\w+)/$', 'pantoto.views.post_pagelet'),
    
    (r'^pagelet/$', 'pantoto.views.list_pagelet'),

    (r'^pagelet/get_pagelets/$', 'pantoto.views.get_pagelets'),

    (r'^view/$', 'pantoto.views.list_views'),

    (r'^view/add/$', 'pantoto.views.add_view'),
    
    (r'^view/(?P<view_id>\w+)/delete/$', 'pantoto.views.delete_view'),

    (r'^view/(?P<view_id>\w+)/$', 'pantoto.views.edit_view'),

    (r'^view/(?P<view_id>\w+)/get_fal/$', 'pantoto.views.get_view_fal'),

    (r'^view/(?P<view_id>\w+)/delete/$', 'pantoto.views.delete_view'),

    (r'^category/$', 'pantoto.views.list_categories'),

    (r'^category/add/$', 'pantoto.views.add_category'),

    (r'^category/(?P<category_id>\w+)/$', 'pantoto.views.edit_category'),

    (r'^category/(?P<category_id>\w+)/delete/$', 'pantoto.views.delete_category'),

    (r'^site/$', 'pantoto.views.list_sites'),

    (r'^site/add/$', 'pantoto.views.add_site'),

    (r'^site/(?P<site_id>\w+)/$', 'pantoto.views.edit_site'),

    (r'^site/(?P<site_id>\w+)/delete/$', 'pantoto.views.delete_site'),

    (r'^site/(?P<site_id>\w+)/view/$', 'pantoto.views.view_site'),

    (r'^help/$', 'pantoto.views.get_help'),
)


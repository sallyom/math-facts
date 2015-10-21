from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

import views

urlpatterns = patterns('',
    url(r'^$', views.show_flashcard, name='show_flashcard'),
    url(r'^post/$', views.post_flashcard, name='post_flashcard'),
    url(r'^reset/$', views.reset_stats, name='reset_stats'),

    url(r'^list/$', views.list_flashcards, name='list_flashcards'),
    url(r'^table/$', views.show_table, name='table'),

    url(r'^panel/$', views.control_panel, name='control_panel'),
    url(r'^panel/maxterm/(?P<value>\d+)/$', views.change_controls, {'key': 'maxterm'}, name='change_maxterm'),
    url(r'^panel/operation/(?P<value>\w+)/$', views.change_controls, {'key': 'operation'}, name='change_operation'),
    url(r'^panel/timeout/(?P<value>\w+)/$', views.change_controls, {'key': 'timeout'}, name='change_timeout'),

    url(r'^panel/flashcard_list/edit/$', views.edit_flashcard_list, name='edit_flashcard_list'),
    url(r'^panel/flashcard_list/post/$', views.post_flashcard_list, name='post_flashcard_list'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'math/login.html'}, name='math_login'),
    url(r'^logout/$', views.math_logout, name='math_logout'),
)

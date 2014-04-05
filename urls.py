from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

import views

urlpatterns = patterns('',
    url(r'^$', views.show_flashcard, name='show_flashcard'),
    url(r'^post/$', views.post_flashcard, name='post_flashcard'),
    url(r'^reset/$', views.reset_stats, name='reset_stats'),

    url(r'^facts/$', views.show_facts, name='facts'),
    url(r'^table/$', views.show_table, name='table'),

    url(r'^panel/$', views.control_panel, name='control_panel'),
    url(r'^panel/magnitude/(?P<value>\d+)/$', views.change_controls, {'key': 'magnitude'}, name='change_magnitude'),
    url(r'^panel/operation/(?P<value>\w+)/$', views.change_controls, {'key': 'operation'}, name='change_operation'),

    url(r'^index/$', views.index, name='index'),
)

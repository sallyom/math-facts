from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

import views

urlpatterns = patterns('',
    url(r'^math/$', views.index, name='index'),
    url(r'^math/facts/(?P<order>\d+)?/?$', views.show_facts, name='facts'),
    url(r'^math/table/(?P<order>\d+)?/?$', views.show_table, name='table'),
)

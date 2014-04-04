from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

import views

urlpatterns = patterns('',
    url(r'^$', views.show_flashcard, name='show_flashcard'),
    url(r'^post/$', views.post_flashcard, name='post_flashcard'),
    url(r'^reset/$', views.reset_flashcard_stats, name='reset_flashcard_stats'),

    url(r'^facts/$', views.show_facts, name='facts'),
    url(r'^table/$', views.show_table, name='table'),
    
    url(r'^magnitude/(?P<magnitude>\d+)?/?$', views.change_magnitude, name='change_magnitude'),
    
    url(r'^navigation/$', views.index, name='index'),
)

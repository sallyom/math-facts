from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

import views

urlpatterns = patterns('',
    url(r'^math/$', views.show_flashcard, name='show_flashcard'),
    url(r'^math/post/$', views.post_flashcard, name='post_flashcard'),
    url(r'^math/reset/$', views.reset_flashcard_stats, name='reset_flashcard_stats'),

    url(r'^math/facts/$', views.show_facts, name='facts'),
    url(r'^math/table/$', views.show_table, name='table'),
    
    url(r'^math/magnitude/(?P<magnitude>\d+)?/?$', views.change_magnitude, name='change_magnitude'),
    
    url(r'^math/navigation/$', views.index, name='index'),
)

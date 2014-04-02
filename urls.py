from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

import views

urlpatterns = patterns('',
    url(r'^math/$', views.index, name='index'),
    url(r'^math/facts/$', views.show_facts, name='facts'),
    url(r'^math/table/$', views.show_table, name='table'),
    
    url(r'^math/order/(?P<order>\d+)?/?$', views.change_order, name='change_order'),
    
    url(r'^math/flashcard/$', views.show_flashcard, name='show_flashcard'),
    url(r'^math/flashcard/post/$', views.post_flashcard, name='post_flashcard'),
)

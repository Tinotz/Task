from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^(?P<PK>\d+)/item$', ItemList.as_view(), name='ItemList'),
    url(r'^create/item$', ItemList.as_view(), name='ItemList'),

]
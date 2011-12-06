from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'bbconfig.views.index', name='index'),
    url(r'^project/(\d+)/$', 'bbconfig.views.project', name='project'),
)

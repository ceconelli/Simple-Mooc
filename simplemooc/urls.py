from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('simplemooc.core.urls',namespace='core')),
    url(r'^cursos/', include('simplemooc.courses.urls',namespace='courses')),
    url(r'^admin/', include(admin.site.urls)),
)
#name é o nome da url, ou seja, se um template quiser acessar uma url especifica, ele deve
#procurar por esse name, com a seguinte tag href="{% url nomedaurl %}"
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
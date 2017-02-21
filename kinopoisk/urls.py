"""kinopoisk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('movies:movies_list'))),
    url(r'^movies/', include('movies.urls', namespace='movies')),
    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('core.urls', namespace='core')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

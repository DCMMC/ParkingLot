"""parking_lot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import add, search, login_handler, logout_handler, log_state
from .views import debug_url
from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.static import serve
from parking_lot.settings import MEDIA_ROOT, NOT_FOUND_ROOT, LOGIN_ROOT
from parking_lot.settings import MODELS_ROOT
from django.conf.urls import (
    handler404
)
from django.contrib.auth.decorators import login_required

handler404 = 'parking_lot.views.page_not_found' # noqa

urlpatterns = [
    path('admin_django/', admin.site.urls),
    path('addData', add),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^index.html$', TemplateView.as_view(template_name="index.html")),
    path('admin.html', TemplateView.as_view(
        template_name="admin.html")),
    path('client-indoor.html', login_required(TemplateView.as_view(
        template_name="client-indoor.html"))),
    path('client-outdoor.html', login_required(TemplateView.as_view(
        template_name="client-outdoor.html"))),
    path('query', login_required(search)),
    url(r'^media/(?P<path>.*)$', login_required(serve), {
            'document_root': MEDIA_ROOT,
        }),
    url(r'^models/(?P<path>.*)$', login_required(serve), {
            'document_root': MODELS_ROOT,
        }),
    url(r'^404/(?P<path>.*)$', serve, {
            'document_root': NOT_FOUND_ROOT,
        }),
    url(r'^login/(?P<path>.*)$', serve, {
            'document_root': LOGIN_ROOT,
        }),
    path('login_handler', login_handler),
    path('logout_handler', logout_handler),
    path('log_state', log_state),
    path('debug', debug_url),
]

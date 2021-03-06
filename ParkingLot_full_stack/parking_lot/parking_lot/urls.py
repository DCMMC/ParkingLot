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
from .views import login_handler, logout_handler, log_state
from .views import admin_logout
from .views import get_member_cards
from .views import add_member_card
from .views import rm_member_card
from .views import update_member_card
from .views import admin_login
from .views import admin_info
from .views import update_vehicle
from .views import get_vehicles_filter
from .views import debug_url
from .views import parking_lot_status_update
from .views import get_parkings_filter
from .views import update_parking
from .views import get_parking_logs_filter
from .views import get_card_logs_filter
from django.conf.urls import url
from .views import add_vehicle
from .views import rm_vehicle
from .views import get_bill_log_filter
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
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^index.html$', TemplateView.as_view(template_name="index.html")),
    path('admin.html', TemplateView.as_view(
        template_name="admin.html")),
    path('client-indoor.html', login_required(TemplateView.as_view(
        template_name="client-indoor.html"))),
    path('client-outdoor.html', login_required(TemplateView.as_view(
        template_name="client-outdoor.html"))),
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
    path('user/login', admin_login),
    path('user/logout', admin_logout),
    path('user/info', admin_info),
    path('parking_lot_status_update', parking_lot_status_update),
    path('getParkingsFilter', get_parkings_filter),
    path('updateParking', update_parking),
    path('addVehicle', add_vehicle),
    path('rmVehicle', rm_vehicle),
    path('updateVehicle', update_vehicle),
    path('getVehicleFilter', get_vehicles_filter),
    path('getBillLogFilter', get_bill_log_filter),
    path('getMemberCard', get_member_cards),
    path('addMemberCard', add_member_card),
    path('rmMemberCard', rm_member_card),
    path('updateMemberCard', update_member_card),
    path('getMemberCardLog', get_card_logs_filter),
    path('getParkingLotLog', get_parking_logs_filter)
]

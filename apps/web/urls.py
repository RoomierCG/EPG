from django.urls import path, include
from . import views
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [

    # DJANGO REST FRAMKEWORK
    path('api-auth/', include("rest_framework.urls"), name='rest_framework'),

    # this route catches the "naked" URL with no path specified. you can link to it in most places
    path(r'', views.MyReactView.as_view(), name='react_app'),

    # this route catches any url below the main one, so the path can be passed to the front end
    path(r'<path:path>', views.MyReactView.as_view(), name='react_app_with_path'),
]
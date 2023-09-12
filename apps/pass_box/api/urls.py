from django.urls import path
from . import views
from rest_framework import routers


app_name = 'pass_box'

route = routers.DefaultRouter()
route.register('box', views.PassViewSet, basename='passes')
route.register('share', views.ShareViewSet, basename='shares')

urlpatterns = [
]

urlpatterns += route.urls

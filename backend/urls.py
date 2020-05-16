"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .api.views import index_view, MessageViewSet, ImageViewSet
from .api.views import UserList, UserDetail, AnnotationViewSet

router = routers.DefaultRouter()
router.register('messages', MessageViewSet)
router.register('images', ImageViewSet)
router.register('annotations', AnnotationViewSet)

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    # api authentication
    path('api/auth/', include('rest_framework.urls')),

    # user
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]

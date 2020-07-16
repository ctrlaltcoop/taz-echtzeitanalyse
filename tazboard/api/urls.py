from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

from .views import HistogramView, RedocView, ReferrerView, DevicesView, ToplistView

api_patterns = [
    path('histogram', HistogramView.as_view(), name='histogram'),
    path('referrer', ReferrerView.as_view(), name='referrer'),
    path('toplist', ToplistView.as_view(), name='toplist'),
    path('devices', DevicesView.as_view(), name='devices')
]

urlpatterns = [
  path('schema', get_schema_view(
      title='taz website metrics API',
      public=True,
      permission_classes=[AllowAny],
      patterns=api_patterns
  ), name='api_v1_schema'),
  path('redoc', RedocView.as_view(), name='redoc')
] + api_patterns

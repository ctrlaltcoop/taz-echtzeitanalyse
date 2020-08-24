from django.urls import path, re_path
from django.views.generic import RedirectView

from tazboard.frontend import views

urlpatterns = [
    re_path(r'^$', RedirectView.as_view(url='app', permanent=False), name='index'),
    path('app', views.FrontendView.as_view()),
]

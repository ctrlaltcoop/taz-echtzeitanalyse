from django.urls import path

from tazboard.frontend import views

urlpatterns = [
    path('app', views.FrontendView.as_view()),
]

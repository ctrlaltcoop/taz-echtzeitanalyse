from django.urls import path

from frontend import views

urlpatterns = [
    path('app', views.FrontendView.as_view()),
]

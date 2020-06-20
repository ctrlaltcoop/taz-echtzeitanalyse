from django.shortcuts import render
from django.views.generic import TemplateView


class FrontendView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'frontend/index.html')

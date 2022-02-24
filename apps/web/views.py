from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

@method_decorator(csrf_exempt, name="dispatch")
class MyReactView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'context_variable': 'value'}
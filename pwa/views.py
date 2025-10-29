from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader

class ServiceWorkerView(TemplateView):
    template_name = 'pwa/sw.js'
    content_type = 'application/javascript'

class ManifestView(TemplateView):
    template_name = 'pwa/manifest.json'
    content_type = 'application/json'

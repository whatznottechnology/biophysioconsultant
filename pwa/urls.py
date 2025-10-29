from django.urls import path
from .views import ServiceWorkerView, ManifestView

urlpatterns = [
    path('sw.js', ServiceWorkerView.as_view(), name='service_worker'),
    path('manifest.json', ManifestView.as_view(), name='manifest'),
]

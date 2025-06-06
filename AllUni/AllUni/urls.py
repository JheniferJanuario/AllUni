from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='users/home.html'), name='home'),
    path('', include('users.urls')),
    path('subjects/', include('subjects.urls')),
]

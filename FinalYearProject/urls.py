from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import TemplateView
from . import model_creation

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('Foodie.urls')),
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
	url(r'^oauth/', include('social_django.urls', namespace='social')),

]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

#model_creation.create()

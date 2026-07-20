from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/', permanent=False)),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    path('api/', include('LittleLemonAPI.urls')),

    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken')),

]

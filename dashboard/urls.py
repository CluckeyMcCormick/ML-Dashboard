"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from django.contrib import admin

from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings

urlpatterns = [
	#redirect to admin site
    url(r'^admin/', admin.site.urls),
    #redirect all contact requests to the contact app
    url(r'^contact_app/', include('contact.urls')),
    #Actually, let's just redirect all unspecified traffic to the contact app
    url(r'^$', RedirectView.as_view(url='/contact_app/', permanent=True)),
    #For some reason, my browser keeps routing to catalog
    #A fix, perhaps?
    url(r'^catalog/', RedirectView.as_view(url='/contact_app/', permanent=True)),
    url(r'^contact/', RedirectView.as_view(url='/contact_app/', permanent=True)),
    #Authentication fun
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
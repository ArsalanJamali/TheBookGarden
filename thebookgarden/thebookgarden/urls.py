"""thebookgarden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import HomePage,ContactUsView,AboutUsView,CartDisplayView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomePage.as_view(),name="index"),
    path('products/',include('product_app.urls')),
    path('',include('customer_app.urls')),
    path('contact-us/',ContactUsView,name='contact-us'),
    path('about-us/',AboutUsView.as_view(),name='about-us'),
    path('cart/',CartDisplayView,name='cart-display')
]

urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.book, name='book')
Class-based views
    1. Add an import:  from other_app.views import Book
    2. Add a URL to urlpatterns:  path('', Book.as_view(), name='book')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book.urls', namespace='book')),
    path('account/', include('account.urls', namespace='account')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('order/', include('order.urls', namespace='order')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

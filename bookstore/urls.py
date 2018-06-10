"""stars_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from stars_task import settings
from . import views

urlpatterns = [
    url(r'^$', views.book_list, name='book_list'),
    url(r'^new_book/$', views.create_book, name='create_book'),
    url(r'^contact/(?P<pk>\d+)/$', views.edit_book, name='edit_book'),
    url(r'^view_logs/$', views.view_logs, name='view_logs'),
    url(r'^view_requests/$', views.view_10_request, name='view_requests'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
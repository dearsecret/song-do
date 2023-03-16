"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

# from django.conf import settings
# from django.conf.urls.static import static

admin.site.site_header = "송도 관리자"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/contracts/", include("contracts.urls")),
    path("api/v1/invoices/", include("bills.urls")),
    path("api/v1/notices/", include("notices.urls")),
    path("api/v1/informations/", include("informations.urls")),
    path("api/v1/promotions/", include("promotions.urls")),
]

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

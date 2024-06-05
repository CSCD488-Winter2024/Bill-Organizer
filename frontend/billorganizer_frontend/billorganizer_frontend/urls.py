"""
URL configuration for billorganizer_frontend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from bill_app import views
from django.urls import path, include
from bill_app.components.bill_add import BillAddView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")), 
    path("accounts/", include("django.contrib.auth.urls")),
    path("unicorn/", include("django_unicorn.urls")),
    path('',views.index, name="homepage"),
    path('bills/',views.allbills, name="billpage"),
    path("search/", views.SearchResultsView, name="search_results"),
    path("mybills/", views.mybills, name="my_bills"),
    path("billadd/", views.bill_add, name="bill_add"),
    path("billbutton/", views.bill_button, name="bill_button"),
    path("addall/", views.add_all_button, name="add_all_button"),
    path("getnote/<str:biennium>/<str:bill_id>/", views.get_note, name="get_note"),
    path("writenote/<str:biennium>/<str:bill_id>/", views.write_note, name="write_note"),
]

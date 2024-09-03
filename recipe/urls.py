"""
URL configuration for recipe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from recipeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('login/',views.login1),
    path('signup/',views.signup1),
    path('view/',views.view),
    path('add/',views.adddish),
    path('full_recipe/<recipe_id>/', views.recipe),
    path('edit/<edit_id>/',views.edit),
    path('delete/<delete_id>/',views.delete),
    path('logout/',views.logout_view),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


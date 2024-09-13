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
    path('', views.home, name='home'),
    path('login/', views.login1, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup1, name='signup'),
    path('view/', views.view, name='view'),
    path('add/', views.adddish, name='add'),
    path('edit/<int:edit_id>/', views.edit, name='edit'),
    path('delete/<int:delete_id>/', views.delete, name='delete'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('notifications/', views.notifications, name='notifications'),
    path('user_recipe/<id>',views.user_recipe),
    path('profile/<id>',views.profile_view,name='profile_view'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('save/<id>/', views.save,name='save'),
    path('saved_recipe/', views.view_saved),
    path('following/',views.following,name='following'),
    path('rate/<int:id>/<rate>/',views.rate,name='rate'),
    path('profile_edit/<id>',views.profile_edit_view),
    path('recommender/',views.recommender,name='recommender'),
    path('home/',views.recommendationPage,name='rp'),
    path('search/', views.search_recipes, name='search_recipes'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


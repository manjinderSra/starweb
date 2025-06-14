"""
URL configuration for StartWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from StartApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.Home.as_view(), name='home'),
    path('register', views.Register.as_view(), name='register'),
    path('login', views.ViewLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('create_article', views.CreateArticle.as_view(), name='create_article'),
    path('CategoryArticle', views.CategoryArticle.as_view(), name='CategoryArticle'),
    path('TagCreate', views.TagCreate.as_view(), name='TagCreate'),
    path('ReadArticle/<int:pk>', views.ReadArticle.as_view(), name='ReadArticle'),
    path('EditArticle/<int:id>', views.EditArticle.as_view(), name='EditArticle'),
    path('api/articles/', views.ArticleListAPI.as_view(), name='api-article-list'),
    path('api/articles_details/', views.ArticleDetailAPI.as_view(), name='create_new'),
    path('api/articles_details/<int:id>', views.ArticleDetailAPI.as_view(), name='article-detail'),
    path('api/categories/', views.CategoryDetailAPI.as_view(), name='CategoryDetailAPI'),
    path('api/categories/<int:id>', views.CategoryDetailAPI.as_view(), name='CategoryDetailAPI'),
    path('api/TagDetail/', views.TagDetailAPI.as_view(), name='TagDetailAPI'),
    path('api/users/', views.UserListAPI.as_view(), name='user-list'),
    path('api/register/', views.UserRegisterAPI.as_view(), name='user-register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
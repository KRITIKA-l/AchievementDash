"""
URL configuration for project3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from student import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('search/', views.search, name='search'),
    
    path('dashboard',views.dashboard,name='dashboard'),
    path('addachievement',views.addachievement,name='addachievement'),

    path('loginuser/',views.loginuser,name='loginuser'),
    path('signupuser/',views.signupuser,name='signupuser'),
    path('logoutuser/',views.logoutuser,name='logoutuser'),
    
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    

    path("opportunities/", views.opportunity_list, name="opportunity_list"),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunity/<int:pk>/apply/', views.apply_for_opportunity, name='apply_for_opportunity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


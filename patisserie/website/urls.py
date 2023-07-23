from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('browse/', views.browse_items, name='browse_items'),
    path('guest_browse/', views.guest_browse_items, name='guest_browse_items'),
    path('add_item/', views.add_item, name='add_item'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_all_from_cart/', views.remove_all_from_cart, name='remove_all_from_cart'),
]
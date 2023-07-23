# your_project_name/urls.py
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from website import views as website_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/', include('website.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/profile/', website_views.profile, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cart/', website_views.view_cart, name='cart'),  # Use website_views here
    path('remove_all_from_cart/', website_views.remove_all_from_cart, name='remove_all_from_cart'),  # Use website_views here
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
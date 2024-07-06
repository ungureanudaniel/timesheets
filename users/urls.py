from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from users.views import register, profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('register/', register, name='register'),
        path('profile/', profile, name='profile'),
        path('inactive-profile/', profile, name='awaiting-approval'),
        path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
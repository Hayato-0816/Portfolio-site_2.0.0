from django.urls import path
from . import views
from blog.views import PostListView
from gallery.views import GalleryView

app_name = 'dashboard'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('blog/', PostListView.as_view(), name='blog_list'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
]  
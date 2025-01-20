from django.urls import path
from . import views
from blog.views import PostListView, PostDetailView

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/post/', PostListView.as_view(), name='post_list'),
    path('blog/post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
] 

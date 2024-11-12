from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('blog/manage/', views.BlogmanagementView.as_view(), name='blog_management'),
    path('blog/manage/category/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('blog/manage/post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('blog/manage/post/create/', views.PostCreateView.as_view(), name='post_create'),
]  
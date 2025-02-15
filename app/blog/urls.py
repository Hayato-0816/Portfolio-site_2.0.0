from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('search/', views.SearchView, name='search'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]

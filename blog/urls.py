from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog_home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.PostDetailView.as_view(), name='post_detail'),
]

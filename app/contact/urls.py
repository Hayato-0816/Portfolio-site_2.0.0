from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.MessageView.as_view(), name='message'),
]
    
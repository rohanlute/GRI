from django.urls import path
from .views import *

app_name = "notifications"

urlpatterns = [
    path('notification_list/',NotificationListView.as_view(),name='notification_list'),
]
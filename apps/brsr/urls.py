from django.urls import path
from .views import brsr_list

app_name = "brsr"

urlpatterns = [path('brsr-list/', brsr_list, name='brsr_list'),]
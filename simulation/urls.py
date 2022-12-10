from django.urls import path
from . import views

app_name = 'simulation'

# url routes list
urlpatterns = [
    # path --> domain.com / simulation /
    # /my_apps --> PROJECT urls.py
    path('calculator/', views.calculator, name='calculator'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('regulations/', views.regulations, name='regulations'),
    path('info/', views.info, name='info'),
]
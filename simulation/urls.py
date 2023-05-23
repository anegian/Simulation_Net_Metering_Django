from django.urls import path
from . import views

app_name = 'simulation'

# url routes list
urlpatterns = [
    # path --> domain.com / simulation /
    # /my_apps --> PROJECT urls.py

    path('calculator/', views.calculator_forms_choice, name='calculator'),
    path('dashboard/', views.dashboard_results, name='dashboard'),
    path('regulations/', views.regulations, name='regulations'),
    path('about/', views.about, name='about'), 
    path('signup/', views.signup, name='signup'),
]

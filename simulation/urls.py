from django.urls import path
from . import views

app_name = 'simulation'

# url routes list
urlpatterns = [
    # path --> domain.com / simulation /
    # /my_apps --> PROJECT urls.py

<<<<<<< HEAD
    path('ajax/', views.calculate_power, name='calculate_power'),
=======
>>>>>>> 8df12127ee48ab232b6828d149c92dcbf825a3d2
    path('calculator/', views.calculator_forms_choice, name='calculator'),
    path('dashboard/', views.dashboard_results, name='dashboard'),
    path('regulations/', views.regulations, name='regulations'),
    path('about/', views.about, name='about'), 
    path('signup/', views.signup, name='signup'),
<<<<<<< HEAD

=======
>>>>>>> 8df12127ee48ab232b6828d149c92dcbf825a3d2
]



from django.urls import path
from . import views

from loans.views import apply_loan

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('',views.login,name ='login'),
    path('logout/', views.logout, name='logout'),
    # path('apply_loan/', apply_loan,name='apply_loan')
]
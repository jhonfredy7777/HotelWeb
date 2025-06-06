from django.urls import path
from user import views



urlpatterns = [
    path('', views.VRegister.as_view(), name="Authentication" ),
    path('login/', views.log_in, name="Login" ),
    path('logout/', views.log_out, name="Logout" ),
    path('customer_profile/', views.customer_profile, name="Customer_profile" ),
    path('customer_reservations/', views.customer_reservations, name="Customer_reservations" ),

    






]


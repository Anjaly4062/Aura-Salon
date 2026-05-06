"""
URL configuration for salon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from salonapp.views import login_view,admin_home,staff_home,customer_home,add_service,view_services,home,edit_service,delete_service,service_detail,book_service,my_bookings,add_staff,view_customers,view_staff,admin_view_services,logout_view,complete_booking,register_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('login/', login_view, name='login'),
     path('admin_home/', admin_home, name='admin_home'),
    path('staff_home/', staff_home, name='staff_home'),
    path('customer_home/', customer_home, name='customer_home'),
    path('add_service/',add_service,name='add_service'),
    path('view_services/',view_services,name='view_services'),
    path('edit_service/<int:id>/', edit_service, name='edit_service'),
    path('delete_service/<int:id>/', delete_service, name='delete_service'),
    path('customer_home/', customer_home, name='customer_home'),
    path('service_detail/<int:id>/', service_detail, name='service_detail'),
    path('book_service/<int:id>/', book_service, name='book_service'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    path('add_staff/', add_staff, name='add_staff'),
    path('view_customers/', view_customers, name='view_customers'),
    path('view_staff/', view_staff, name='view_staff'),
    path('admin_services/', admin_view_services, name='admin_view_services'),
    path('logout/', logout_view, name='logout'),
    path('complete_booking/<int:id>/', complete_booking, name='complete_booking'),
    path('register/', register_view, name='register')
    
]

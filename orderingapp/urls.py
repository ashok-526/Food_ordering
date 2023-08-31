"""
URL configuration for orderingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from food import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login_page, name='login'),
    path('add-card/<pizza_uid>', views.add_card , name='add-card'),
    path('register/',views.register, name='register'),
    path('',views.order_home, name='order'),
    path('cart/' , views.cart, name='cart'),
    path('DashBoard/', views.dashboard , name='DashBoard'),
    path('order-place/' , views.order_info , name='order_info'),

    path('payment/<str:order_uid>/', views.payment, name='payment'),

    path('remove_item/<remove_item>',views.remove_item , name='remove_item')
]







if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



urlpatterns += staticfiles_urlpatterns()
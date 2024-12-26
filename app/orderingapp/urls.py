from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from food import views

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),

    # Application URLs
    path('', views.order_home, name='order'),
    path('cart/', views.cart, name='cart'),
    path('DashBoard/', views.dashboard, name='DashBoard'),
    path('order-place/', views.order_info, name='order_info'),
    path('payment/<str:order_uid>/', views.payment, name='payment'),
    path('add-card/<str:pizza_uid>/', views.add_card, name='add-card'),
    path('remove_item/<str:remove_item>/', views.remove_item, name='remove_item'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Serve static and media files manually when DEBUG is False
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.order_list),
    path('orders/<str:pk>/', views.order_detail),
    path('accounts/',views.profile_view,)
]
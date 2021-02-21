from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/access/', TokenRefreshView.as_view(), name='token_get_access'),
    path('token/both/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('orders/', views.order_list),
    path('orders/<str:pk>/', views.order_detail),
    path('accounts/',views.profile_view,),
    path('myaccount/',views.my_profile_view,),
    path('userexists/',views.UserExistsView.as_view(),name='User exists check')


]
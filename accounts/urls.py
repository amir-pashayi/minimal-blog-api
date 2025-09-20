from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegisterView.as_view(), name='login_register'),
    path("me/profile/", views.MyProfileView.as_view(), name="my-profile"),
    path("<str:username>/profile/", views.ProfileView.as_view(), name="public-profile"),
    path("<str:username>/block/", views.BlockUserView.as_view(), name="user-block"),

]

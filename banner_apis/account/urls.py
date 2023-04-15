from django.urls import path, include
from account.views import * #serRegistrationView,AdminBannerModelViewSet UserLoginView, UserLogoutView,CategoryModelViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'category', CategoryModelViewSet)
router.register(r'admin_banners', AdminBannerModelViewSet)

urlpatterns = [
    #user
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('validate_otp/', ValidateOTP.as_view()),
    path('getalluser/', UserRegistrationView.as_view(), name='getalluser'),
    path('updateuser/<int:id>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='updateuser'),
    path('getuser/<int:id>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='getuser'),
    path('deleteuser/<int:id>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='deleteuser'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('resend-otp/', ResendUserOtpAPIView.as_view(), name='change-password'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    #banner   
    path('add_banners/', BanerAPIView.as_view(), name='addbanner'),
    path('category_banners/<int:category_id>/', GetCategoryBanners.as_view(), name='addbanner'),
    path('get_all_banners/', BanerAPIView.as_view(), name='getalluser'),
    path('get_banner/<int:id>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='get_banner'),
    path('update_banner/<int:id>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='updatebanner'),
    path('delete_banner/<int:id>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='deletebanner'),
    
    #category
    path('', include(router.urls)),
    
    

]

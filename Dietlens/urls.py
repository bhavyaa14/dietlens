"""
URL configuration for Dietlens project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from user_app.views import *
from diet_advisor.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',SignupView.as_view(),name = "signup"),
    path('signin/',SigninView.as_view(),name="signin"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('forgot/',ForgotpasswordView.as_view(),name ="forgot"),
    path('verify/',OtpverifyView.as_view(),name="verify"),
    path('reset/',ResetpasswordView.as_view(),name="reset"),
    path('',BaseView.as_view(),name= "home"),
    path('createprofile/',UserprofileCreateView.as_view(),name="createprofile"),
    path('update/<int:pk>',UserProfileUpdateView.as_view(), name="update"),
    path('detailprofile/',UserProfileDetailView.as_view(),name='detail_profile'),
    path('deleteprofile/<int:pk>',UserprofiledeleteView.as_view(),name='delete_profile'),
    path('result/', UserProfileResultView.as_view(), name="profile_result"),
    path("upload/",FoodLogView.as_view(),name="upload"),
    path('foodresult/<int:pk>',FoodresultView.as_view(),name="result"),
    path('premium_order/',CreatePremiumView.as_view(),name="premium"),
    path('payment_success/',PaymentSuccessView.as_view(), name="success")
    
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




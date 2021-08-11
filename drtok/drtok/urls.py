"""drtok URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
# from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from .usrt import admin
from .usrt import views as accounts

# rest_framework automatic URL routing.
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

# include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', accounts.customer_login, name='login'),
    path('accounts/logout/', accounts.BlacklistTokenView, name='logout'),
    path('accounts/profile/',accounts.profile),
    path('accounts/register/', accounts.register, name = 'register'),
    path('token/refresh/', TokenRefreshView.as_view(),name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(),name="token_verify"),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/users/', views.ListUsers.as_view()),
    # path('', views.UserAPI.as_view()),
    # path('<int:pk>', views.UserRetrieveUpdateDestroyAPI.as_view()),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
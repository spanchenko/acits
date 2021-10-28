from django.urls import path, include
from api.views import RegisterView, UserViewSet, FlatViewSet, RentOrderViewSet, RoomViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_nested import routers

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('flats', FlatViewSet, basename='flats')
router.register('order', RentOrderViewSet, basename='order')

flat_router = routers.NestedSimpleRouter(router, 'flats', lookup='flats')
flat_router.register('rooms', RoomViewSet, basename='flat-rooms')


urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
] + router.urls + flat_router.urls

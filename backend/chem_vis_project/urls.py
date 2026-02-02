"""
URL configuration for chem_vis_project project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from api.views import DataSetViewSet, MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API paths
    path('api/datasets/data/', DataSetViewSet.as_view({'get': 'data'}), name='dataset-data'),
    path('api/datasets/generate_report/', DataSetViewSet.as_view({'get': 'generate_report'}), name='dataset-generate-report'),
    path('api/datasets/', DataSetViewSet.as_view({'get': 'list', 'post': 'create'}), name='dataset-list'),
    path('api/datasets/<int:pk>/', DataSetViewSet.as_view({'get': 'retrieve'}), name='dataset-detail'), # This can still be useful

    # Token paths
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

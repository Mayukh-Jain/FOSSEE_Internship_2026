from django.urls import path
from .views import DataSetViewSet

dataset_list = DataSetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

dataset_detail = DataSetViewSet.as_view({
    'get': 'retrieve',
})

dataset_data = DataSetViewSet.as_view({
    'get': 'data'
})

dataset_report = DataSetViewSet.as_view({
    'get': 'generate_report'
})

urlpatterns = [
    path('datasets/', dataset_list, name='dataset-list'),
    path('datasets/<int:pk>/', dataset_detail, name='dataset-detail'),
    path('datasets/<int:pk>/data/', dataset_data, name='dataset-data'),
    path('datasets/<int:pk>/generate_report/', dataset_report, name='dataset-generate-report'),
]

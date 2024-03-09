from django.urls import path
from .views import ProductView, ProductSubCategoryView  # , viewProduct

app_name = 'product'

urlpatterns = [
    path('', ProductView.as_view({'get': 'list'}),),
#     path('create/', ProductView.as_view({'post': 'create'}),),
    path('<int:pk>/', ProductView.as_view({'get': 'retrieve'}),),
    path('sub-category/<int:pk>/',
         ProductSubCategoryView.as_view({'get': 'list'}), name='sub_category'),
]

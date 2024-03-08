from django.urls import path
from .views import ProductView, ProductSubCategoryView  # , viewProduct

app_name = 'product'

urlpatterns = [
    path('', ProductView.as_view({'get': 'list'}),),
    path('create/', ProductView.as_view({'post': 'create'}),),
    path('<int:pk>/', ProductView.as_view({'get': 'retrieve'}),),
    path('store/<int:store_id>/',
         ProductView.as_view({'get': 'get_store'}), name='store'),
    path('sub-category/<int:pk>/',
         ProductSubCategoryView.as_view(), name='sub_category'),
]

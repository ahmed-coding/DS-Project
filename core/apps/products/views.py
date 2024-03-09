"""_summary_

    Returns:
        _type_: _description_
"""

from django_filters.rest_framework import DjangoFilterBackend
from ..pagination import StandardResultsSetPagination
from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, action
from apps.models import Product, Product_item, Category
from .serializer import ProductSerializer, SingleProductSerializer, DiaaSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from rest_framework import filters
from rest_framework import viewsets
# Create your views here.


class ProductView(viewsets.ModelViewSet):
    """_summary_

    Args:
        ListAPIView (_type_): _description_

    Returns:
        _type_: _description_
    """
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    pagination_class = StandardResultsSetPagination
    ordering_fields = '__all__'
    search_fields = ['product_name', ]
    filterset_fields = ['product_name',]
    # lookup_field = 'pk'
    # lookup_url_kwarg = ['pk', 'store_id']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SingleProductSerializer
        elif self.action == 'create':
            return DiaaSerializer
        else:
            return ProductSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Product.objects.all()
        else:
            return Product.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user} if self.request.user.is_authenticated else {}

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        # user = obj.to_view(
        #     self.request.user) if self.request.user.is_authenticated else None
        return obj

    # def get_queryset(self):
    #     if self.action == 'get_store':
    #         return self.queryset.filter()
    #     return super().get_queryset()


class ProductSubCategoryView(viewsets.ModelViewSet):
    """_summary_

    Args:
        ListAPIView (_type_): _description_
    """
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', ]
    filterset_fields = ['product_name',]
    ordering_fields = '__all__'

    def get(self, request, pk: int):
        """_summary_

        Args:
            request (_type_): _description_
            pk (_type_): _description_

        Returns:
            _type_: _description_
        """
        # if pk == 0 or '0':
        #     return Response({
        #         'error':'This Product dont\'t have a releted Category'
        #     },status=status.HTTP_404_NOT_FOUND)
        try:
            category = Category.objects.get(pk=pk)
            product = Product.objects.filter(category=category)
            ser = self.serializer_class(
                instance=product, many=True).data
            return Response({
                'data': ser.tolist()
            }, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({
                'error': "Sub Category Dose Note Exist"
            }, status=status.HTTP_200_OK)

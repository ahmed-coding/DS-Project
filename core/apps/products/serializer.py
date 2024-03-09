from apps.models import Favorite, Product, Product_item, Rate,  Brand, Image, Cart, User, Promotion
from rest_framework import serializers


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)

    def to_representation(self, instance):
        return instance.image.url

    class Meta:
        model = Image
        fields = ['id', 'image', ]


class ProductItemSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    item_image = ImageSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)
    stock = serializers.SerializerMethodField(read_only=True)
    price = serializers.FloatField()

    def get_stock(self, obj) -> float:
       # rat = obj.stock.stock_qty or False
        try:
            return obj.stock.stock_qty
        except:
            return 0.0
        # # for s in rat:
        # #     sub += s.stock_qty
        # return obj.stock.stock_qty if rat else 0.0

    def get_in_favorite(self, obj) -> bool:
        user = self.context.get('user' or None)
        return obj.favorites.filter(user=user).exists()

    def get_rating(self, obj) -> float:
        rat = obj.rate.all()
        sub = 0.0
        if rat:
            try:
                for s in rat:
                    sub += s.rating
                return sub / rat.count()
            except:
                sub = 0
                return sub
        else:
            return sub

    class Meta:
        model = Product_item
        fields = '__all__'


class DiaaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_item = ProductItemSerializer(read_only=True, many=True)
    category = serializers.SerializerMethodField(read_only=True)
    brand = serializers.SerializerMethodField(read_only=True)
    # product_image = serializers.ImageField(
    #     use_url=True, allow_empty_file=True)

    def validate(self, attrs):
        self.product_item.context = self.context
        return super().validate(attrs)

    def get_brand(self, obj):
        try:
            return obj.brand.brand_name
        except:
            return ""

    def get_category(self, obj) -> str:
        name = ''
        try:
            name = obj.category.name
        except:
            name = "Not Found"
        return name

    class Meta:
        model = Product
        fields = '__all__'


class SingleProductItemSerializer(serializers.ModelSerializer):
    """
    Class Serializers for Single Products_item to get more datils


    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """
    item_image = ImageSerializer(many=True, read_only=True)
    # store = serializers.SerializerMethodField(read_only=True)
    # brand = serializers.SerializerMethodField(read_only=True)
    # sub_category = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)
    price = serializers.FloatField()

    def get_in_favorite(self, obj) -> bool:
        user = self.context.get('user' or None)
        # if isinstance(user, User) else False
        return obj.favorites.filter(user=user).exists()

        # def get_store(self, obj) -> dict:
        #     data = {
        #         'store_name': obj.product.store.store_name,
        #         'id': obj.product.store.id
        #     }
        #     return data

        # def get_brand(self, obj) -> str:
        #     return obj.product.brand.brand_name

        # def get_sub_category(self, obj) -> dict:
        #     data = {}
        #     try:
        #         data['name'] = obj.product.category.name
        #         data['id'] = obj.product.category.id

        #     except:
        #         data['name'] = "Not Found"
        #         data['id'] = 0
        #     return data

    def get_rating(self, obj) -> float:
        rat = obj.rate.all()
        sub = 0.0
        if rat.exists():
            try:
                for s in rat:
                    sub += s.rating
                return sub / rat.count()
            except:
                sub = 0
                return sub
        else:
            return sub

    class Meta:
        model = Product_item
        fields = ['id', 'in_favorite',
                  'rating', 'stock', 'item_image', 'price', 'sku', 'slug']


class SingleProductSerializer(serializers.ModelSerializer):
    """
    SingleProductSerializer for main Product and has Products item 

    Args:
        serializers (_type_): _description_

    Returns:
        _type_: _description_
    """

    product_item = SingleProductItemSerializer(read_only=True, many=True)
    category = serializers.SerializerMethodField(read_only=True)
    brand = serializers.SerializerMethodField(read_only=True)
    product_image = serializers.ImageField(use_url=True)

    def validate(self, attrs):
        self.product_item.context = self.context
        return super().validate(attrs)

    def get_brand(self, obj):
        try:
            return obj.brand.brand_name
        except:
            return ""

    def get_category(self, obj) -> dict:
        data = {}
        try:
            data['name'] = obj.category.name
            data['id'] = obj.category.id

        except:
            data['name'] = "Not Found"
            data['id'] = 0
        return data

    class Meta:
        model = Product
        fields = '__all__'

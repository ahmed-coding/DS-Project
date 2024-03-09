import uuid
from django.utils.text import slugify
from django.contrib.gis.db import models as gis_models
from django.db import models
from PIL import Image as PImage
from xmlrpc.client import TRANSPORT_ERROR
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


# Create your models here.


class MyUserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def _create_user(self,  email, username,  password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(email=email,  username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None,  password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


# ==========


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custome User to create and login user with email and auth_provider like google, facebook or Email.\n
    Auth_provider is default by email.\n

    To Use Choices in auth_provider use  User.EMAIL or User.GOOGLE etc...\n

    AUTHENTICATION:\n
        We use JWT auth for this project
    """
    # Choices
    EMAIL = 'email'
    GOOGLE = 'google'
    FACEBOOB = 'facebook'
    username = models.CharField(
        _("username"),
        max_length=150,
        # unique=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        blank=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    # auth_provider = models.CharField(
    #     max_length=20, blank=True, null=False, default=EMAIL)
    name = models.CharField(
        _('Full name'), max_length=60, default='', blank=True)
    # first_name = models.CharField(
    #     _("first name"), max_length=55, blank=True, default='')
    # last_name = models.CharField(
    #     _("last name"), max_length=55, blank=True, default='')
    # age = models.IntegerField(_('age'), blank=True, null=True)
    # =============
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),  max_length=50, default='', null=True)
    register_data = models.CharField(max_length=20, default='')
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_deleted = models.BooleanField(_('Deleted'), default=False,)
    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now, )
    image = models.ImageField(
        upload_to='user_image',
        # default='user_image/MicrosoftTeams-image.png',
        blank=True,
        null=True
    )

    ########## ManyToMAny Fileds ###########
    # product_view = models.ManyToManyField("Product_item", through='View')
    # wishlist = models.ManyToManyField(
    #     'Product_item', through='Wishlist')
    # favorite = models.ManyToManyField('Product_item', through='Favorite')
    # cart = models.ManyToManyField('Product_item', through='Cart')
    # add_rate = models.ManyToManyField('Product_item', through='Rate')

    objects = MyUserManager()
    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    def get_full_name(self):
        """
        Return the name, with a space in between.
        """
        full_name = "%s " % (self.name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name

    def delete(self, *args, **kwargs):
        """
        Overrid delete method to delete Image first then delete user
        not will be show in admin panle and aothre thinks like auth

        """

        try:
            self.image.delete()
            self.is_deleted = True
            self.is_active = False
            self.is_superuser = False
            self.save()
            return True
        except:
            self.is_deleted = True
            self.save()
            return True

        # return super().delete(*args, **kwargs)
    def get(self,  **kwargs):
        user = self.objects.get(**kwargs, is_delete=False) or None
        if user:
            return user
        raise self.DoesNotExist()

    def __str__(self) -> str:
        return f" {self.pk} |{self.email}:{self.name}"

    # Start Method for Class

    def add_cart(self, item_id: int, count: int):
        try:
            return self.cart.create(product_id=item_id, qty=count)
        except:
            ins = self.cart.get(product_id=item_id)
            ins.qty = count
            return ins.save()

    def add_favorite(self, item_id: int):
        try:
            data = self.favorites.get_or_create(product_id=item_id)
            return data[0]
        except:
            return False

    def remove_favorite(self, item_id: int):
        pass
        # End Method for Class

    class Meta:
        # swappable = "AUTH_USER_MODEL"
        db_table = 'User'
        # verbose_name = 'إدارة المسنخدمين'


class Region(models.Model):
    """
    Region models use a standerd GIS for git polygon
    RSID used is 4326

    Args:
       for add more Region to User from API use json format like this :
    {
        "type": "Point",
        "coordinates": [ 6.328124999119163, 5.195989291152924 ]
    }
    Point X come before Y like [X ,Y] -> Point(X, Y)
    """
    name = models.CharField(max_length=50, default='')
    longitude = models.CharField(_("longitude"), max_length=50)
    latitude = models.CharField(_("latitude"), max_length=50)

    def __str__(self) -> str:
        return f"{self.name} - {self.location} "

    class Meta:
        db_table = 'Region'


class Customer(models.Model):
    recieving_full_name = models.CharField(
        _("recieving_full_name"), max_length=100)
    phone_no = models.CharField(_("phone_no"), max_length=50)
    email = models.CharField(_("email"), max_length=50)

    class Meta:
        db_table = 'Customer'


class User_address(models.Model):
    is_default = models.BooleanField(
        _("is_default"), default=False, blank=True)
    category = models.CharField(_("category"), max_length=50, default="")
    region = models.ForeignKey(Region, verbose_name=_(
        "address"), on_delete=models.PROTECT, related_name='user_address')
    customer = models.ForeignKey(Customer, verbose_name=_(
        "Customer"), on_delete=models.SET_NULL, null=True, blank=True, related_name='user_address')
    user = models.ForeignKey(User, verbose_name=_(
        "user"), on_delete=models.PROTECT, blank=True, related_name='user_address')
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'User_address'


class Notification(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    text = models.TextField(default='')
    # type = models.CharField(max_length=30, default='')
    user = models.ManyToManyField(User, through='User_notification',)
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='notification', )
    time_created = models.DateTimeField(
        _("وقت الانشاء"), auto_now=False, auto_now_add=True)
    is_readed = models.BooleanField(
        _("حالة القرائة"), editable=False, default=False)
    is_pushed = models.BooleanField(_("حالة التلقي"))

    class Meta:
        db_table = 'Notification'


class User_notification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    notification = models.ForeignKey(
        Notification, on_delete=models.PROTECT, related_name='user_notification')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    time_created = models.DateTimeField(
        _("وقت الانشاء"), auto_now=False, auto_now_add=True)
    is_readed = models.BooleanField(
        _("حالة القرائة"), editable=False, default=False)
    is_pushed = models.BooleanField(_("حالة التلقي"))

    class Meta:
        db_table = 'User_notification'
        unique_together = ("notification", "user")


class Category(MPTTModel):
    """
    model for Main category , category and Sub-category in one model
    ----------------
    use parent and level attributes to access who category is returned
    """
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, blank=True, related_name='children', null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category/",)
    Promotions = models.ManyToManyField(
        'Promotion', through='Promotion_category')

    class MPTTMeta:
        # level_attr = 'parint'
        order_insertion_by = ['name']

    def __str__(self):
        return f"name: {self.name} parent {self.parent} id {self.id} "

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

        # img = PImage.open(self.image.path)

        # Resize the image to the desired dimensions (200px width, 140px height)
        # output_size = (200, 140)
        # img.thumbnail(output_size)

        # # Save the resized image
        # img.save(self.image.path)

    class Meta:
        db_table = 'Category'


class Brand(models.Model):
    brand_name = models.CharField(_("brand-name"), max_length=50)

    class Meta:
        db_table = 'Brand'


class Product(models.Model):
    """
    Product Model
    Args:
        models (Product): _description_
    """
    slug = models.SlugField(_("URL id"), unique=True, editable=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    product_name = models.CharField(max_length=50, default="")
    product_image = models.ImageField(
        null=True, blank=True, default='product/download.jpeg', upload_to='products')
    product_description = models.TextField(default='')
    # store = models.ForeignKey(
    #     Store, on_delete=models.CASCADE, related_name='product')
    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, null=True, blank=True, related_name='product')

    def __str__(self) -> str:
        return f"{self.pk} - {self.product_name}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = f"{slugify(self.product_name.strip())}-{str(uuid.uuid4())[:8]}"
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'Product'


class Product_item(models.Model):
    """
    Product Item Model for Product item informations 

    Args:
        models (_type_): _description_
    Returns:
        _type_: _description_
    """
    slug = models.SlugField(_("URL ID"), blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_item')
    # image = models.ImageField(upload_to='products')
    price = models.DecimalField(decimal_places=2, max_digits=16)
    sku = models.ImageField(upload_to='products_sku/', blank=True, null=True)
    # ManytoMany Fialds
    # to_Wishlist = models.ManyToManyField(User, through='Wishlist')
    # to_cart = models.ManyToManyField(User, through='Cart')
    # to_favorite = models.ManyToManyField(User, through='Favorite')
    # to_comment = models.ManyToManyField(User, through='Comment')
    # to_rate = models.ManyToManyField(User, through='Rate')
    # to_view = models.ManyToManyField(User, through='View')

    def __str__(self) -> str:
        return f"{self.pk} | {self.product.id } - "

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = f"{slugify(self.product.product_name.strip(),allow_unicode=True)}-{str(uuid.uuid4())[:12]}"
        return super().save(*args, **kwargs)
# Start Method for class

    def to_wishlist(self, user):
        """add this item to user wishlist
        Args:
            user (User): 
        """

        return user.Product_Wishlist.get_or_create(item=self)

    def to_favorites(self, user):
        """add this item to user favorites
        Args:
            user (User):
        """
        return user.favorites.get_or_create(item=self)

    def to_view(self, user):
        """add this item to user View
        Args:
            user (User):
        """
        return self.view_item.get_or_create(user=user)

    def to_comment(self, user: User, comment: str = ''):
        """add comment user for thisitem 
        Args:
            user (User):
            comment (str):
        Returns:
            Comment: Comment Object
        """
        try:
            obj = self.comment_item.create(user=user, comment=comment)
        except:
            obj = self.comment_item.get(user=user)
            obj.comment = comment
            obj.save()
        return obj

    def to_rate(self, user: User, rate):
        """
        add Rateing of user for this item
        Args:
            user (User): _description_
            rate (Rate): _description_not provide any method handlers 

        Returns:
            Rate: Rate Object
        """
        try:
            obj = self.rate.create(user=user, rating=rate)
        except:
            obj = self.comment_item.get(user=user)
            obj.rating = rate
            obj.save()
        return obj

    def to_cart(self, user_id: int, count: int):
        try:
            return self.item_Cart.create(user_id=user_id, count=count)
        except:
            ins = self.item_Cart.get(user_id=user_id)
            ins.count = count
            return ins.save()

# end Method for class

    class Meta:
        db_table = 'Product_item'


class Image(models.Model):
    date = models.DateField(_("date"), auto_now=True, auto_now_add=False)
    image = models.ImageField(_("image "), upload_to='products_image')
    item = models.ForeignKey(Product_item, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='item_image')

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        print(update_fields)
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        db_table = 'Image'


class Promotion(models.Model):
    promotion_name = models.CharField(max_length=25, default='')
    promotion_description = models.TextField(default='')
    discount_rate = models.FloatField(default=0.0)
    start_date = models.DurationField(blank=True)
    promotion_end_date = models.DurationField(blank=True)
    is_active = models.BooleanField(default=True)
    categorys = models.ManyToManyField(Category, through='Promotion_category')

    def save(self, *args, **kwargs) -> None:
        # self.start_date = datetime.timedelta(days=120)
        # self.promotion_end_date = datetime.timedelta(weeks=1110)
        return super().save(args, kwargs)

    class Meta:
        db_table = 'Promotion'


class Promotion_category(models.Model):
    """
    ManyToMany with Category and Promotion
    """
    promotion = models.ForeignKey(
        Promotion, on_delete=models.PROTECT, related_name='promotion_category')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='promotion_category')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Promotion_category'
        unique_together = ("promotion", "category")


class Variation(models.Model):
    """
    Variation Model

    Args:
        models (_type_): _description_
    """
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='variation')
    value = models.CharField(max_length=30, default='')

    def __str__(self) -> str:
        return f"{self.pk} | - {self.value}"

    class Meta:
        db_table = 'Variation'


class Variation_option(models.Model):
    value = models.CharField(max_length=30, default='')
    variation = models.ForeignKey(
        Variation, on_delete=models.CASCADE, related_name='variation_option')
    item_options = models.ManyToManyField(Product_item, through='Item_option')

    def __str__(self) -> str:
        return f"{self.pk} | {self.variation.id} - {self.value}"

    class Meta:
        db_table = 'Variation_option'


class Item_option(models.Model):
    """
    ManyToMany with  Product_item and variation_option

    Args:
        item => it's Product_item
    """
    item = models.ForeignKey(
        Product_item, on_delete=models.CASCADE, related_name='item_option')
    variation_option = models.ForeignKey(
        Variation_option, on_delete=models.CASCADE, related_name='item_option')

    def __str__(self) -> str:
        return f"{self.pk} | {self.variation_option.id} - {self.item.id}"

    class Meta:
        db_table = 'Item_option'
        unique_together = ("item", "variation_option")


class Stuck(models.Model):
    """
    OneToOne with Product_item

    Args:
        item => it's Product_item
    """
    stuck_type = models.CharField(_("stuck_type"), max_length=50)
    item = models.OneToOneField(
        Product_item, on_delete=models.CASCADE, related_name='stock')

    def __str__(self):
        return f'id:{self.id} - item-id:{self.item.id} '

    class Meta:
        db_table = 'Stuck'


class Favorite(models.Model):
    """
    Favorite model <ManyTOMany> betowen User and Prodect
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    item = models.ForeignKey(
        Product_item, on_delete=models.CASCADE, related_name='favorites')
    time_created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Product- {self.item.id } - User- {self.user.id}"

    class Meta:
        db_table = 'Favorite'
        unique_together = ("item", "user")


class Cart(models.Model):
    """
    Cart model MAnyToMany betowen User and Prodect
    it contains count for number product witsh in Cart
    item => it's Product_item
    """
    item = models.ForeignKey(
        Product_item, on_delete=models.CASCADE, related_name='item_Cart')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name='user_cart')
    count = models.IntegerField(default=1, blank=True)
    time_created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:

        return f"Product- {self.item.id } - User- {self.user.id} - cart-id:{self.id} "

    class Meta:
        db_table = 'Cart'
        unique_together = ("item", "user")


class Rate(models.Model):
    rating_date = models.DateField(auto_now_add=True)
    rating = models.FloatField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rate')
    item = models.ForeignKey(
        Product_item, on_delete=models.CASCADE, related_name='rate')

    class Meta:
        db_table = 'Rate'
        unique_together = ("item", "user")

    def __str__(self):
        return f"id:{self.id} | user-id:{self.user.id} | item-id:{self.item.id}"


class Package(models.Model):
    item_price = models.DecimalField(
        _("item_price"), default=0.0, decimal_places=2, max_digits=16)
    bar_code = models.CharField(_("bar_code"), max_length=50)
    weight = models.FloatField(_("weight"))
    length = models.FloatField(_("length"))
    width = models.FloatField(_("width"))
    dilevery_cost = models.FloatField(_("dilevery_cost"))
    order = models.ForeignKey("Order", verbose_name=_(
        "order"), on_delete=models.CASCADE, related_name='package')

    def __str__(self) -> str:
        return f"{self.order} "

    class Meta:
        db_table = 'Package'
        # unique_together = ("driver", "order")


class Package_catalog(models.Model):
    status_name = models.CharField(_("status_name"), max_length=20)

    def __str__(self) -> str:
        return str(f"status_name: {self.status_name}")

    class Meta:
        db_table = 'Package_catalog'


class Package_status(models.Model):
    """
            Package_status model ManyToMany betowen dilevery and package


    Args:
        models (_type_): _description_
    """
    package_status_note = models.TextField(_("package_status_note"))
    status_time = models.DateTimeField(
        _("status_time"), auto_now_add=True)
    package = models.ForeignKey(Package, verbose_name=_(
        "package"), on_delete=models.CASCADE, related_name='package_status')
    package_catalog = models.ForeignKey(Package_catalog, verbose_name=_(
        "package_catalog"), on_delete=models.CASCADE, related_name='package_status')

    def __str__(self) -> str:
        return str(f"package: {self.package} - package catalog: {self.package_catalog}")

    class Meta:
        db_table = 'Package_status'
        unique_together = ("package", "package_catalog")


class Payment_type(models.Model):
    payment_type_name = models.CharField(_("payment_type_name"), max_length=50)

    def __str__(self) -> str:

        return f"{self.payment_type_name} "

    class Meta:
        db_table = 'Payment_type'


class Payment(models.Model):
    payment_provider = models.CharField(_("payment_provider"), max_length=50)
    payment_date = models.DateTimeField(
        _("payment_date"), auto_now=False, auto_now_add=True)
    payment_type = models.ForeignKey(Payment_type, verbose_name=_(
        "payment_type"), on_delete=models.CASCADE, related_name='payment')
    date = models.DateTimeField(
        _("Date"), auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return str(f"Driver: {self.payment_provider} - payment type: {self.payment_type} - payment date: {self.payment_date}")

    class Meta:
        db_table = 'Payment'


class Payment_details(models.Model):
    """

    Args:
        models (_type_): _description_
    """
    value = models.FloatField(_("value"))
    order = models.ForeignKey(
        "Order", verbose_name=_("order"), on_delete=models.CASCADE, related_name='payment_details')
    payment = models.ForeignKey(Payment, verbose_name=_(
        "payment"), on_delete=models.CASCADE, related_name='payment_details')

    def __str__(self) -> str:
        return str(f"payment: {self.payment} - order:{self.order}")

    class Meta:
        db_table = 'Payment_details'
        unique_together = ("order", "payment")


class Order_type(models.Model):
    type_name = models.CharField(_("type_name"), max_length=50)

    def __str__(self) -> str:

        return f"{self.type_name} "

    class Meta:
        db_table = 'Order_type'


class Order(models.Model):
    order_date = models.DateTimeField(
        _("order_date"), auto_now_add=True)
    discount = models.FloatField(_("discount"))
    packages_price = models.FloatField(_("packages_price"))
    address_shipping = models.ForeignKey(Region, verbose_name=_(
        "address_shipping"), on_delete=models.CASCADE, related_name='order_address_shipping')
    address_billing = models.ForeignKey(Region, verbose_name=_(
        "address_billing"), on_delete=models.CASCADE, related_name='order_address_billing')
    payment_type = models.ForeignKey(Payment_type, verbose_name=_(
        "payment_type"), on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey(User, verbose_name=_(
        "user"), on_delete=models.CASCADE, related_name='order')
    order_type = models.ForeignKey('Order_type', verbose_name=_(
        "order_type"), on_delete=models.CASCADE, related_name='order')

    def __str__(self) -> str:

        return f"id: {self.pk}/ {self.user.name} - {self.order_type.type_name}"

    class Meta:
        db_table = 'Order'

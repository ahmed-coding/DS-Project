from django.contrib import admin
from . import models
# Register your models here.


admin.site.register([models.Variation,
                    models.Variation_option,
                    models.Product_item,
                    models.Product,
                    models.Category
                     ])

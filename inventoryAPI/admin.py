from django.contrib import admin
from .models import *

admin.site.register(Inventory)
admin.site.register(Product)
admin.site.register(ProductPriceHistory)
admin.site.register(InventoryProduct)

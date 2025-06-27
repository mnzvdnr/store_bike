from django.contrib import admin
from .models import Battery_capacity
from .models import Power
from .models import Biks
from .models import Basket
from .models import Customer
from .models import Order
from .models import OrderList



admin.site.register(Battery_capacity)
admin.site.register(Power)
admin.site.register(Biks)
admin.site.register(Basket)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderList)

# @admin.register(Biks)
# class BiksAdmin(admin.ModelAdmin):
#     list_display = ['id_pover', 'id_bc', 'name_bike',
#                     'description_bike', 'price']
#     list_filter = ['id_bc', 'name_bike', 'description_bike']
#     list_editable = ['name_bike', 'price']

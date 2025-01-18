from django.contrib import admin
from dlsApp.models import Sale, Product, SaleItem, StockAdjustment, Expense

# Register your models here.
admin.site.register(Sale)
admin.site.register(Product)
admin.site.register(SaleItem)
admin.site.register(StockAdjustment)
admin.site.register(Expense)


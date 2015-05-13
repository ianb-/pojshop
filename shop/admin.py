from django.contrib import admin
from models import Product, ProductImage, Category, Product_to_cat, Contact, Supplier, PurchaseOrder, PurchaseDetail, Item, SaleOrder, SaleDetail

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Product_to_cat)
admin.site.register(Contact)
admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseDetail)
admin.site.register(Item)
admin.site.register(SaleOrder)
admin.site.register(SaleDetail)
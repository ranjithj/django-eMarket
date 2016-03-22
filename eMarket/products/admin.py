from django.contrib import admin
from .models import Product, Variation, ProductImage, Category, ProductFeatured

# Register your models here.
#class ProductAdmin(admin.ModelAdmin):
 #   date_hierarchy = 'timestamp'
  #  search_fields = ['title', 'description']
   # list_display = ['title', 'price', 'active', 'updated']
    #list_editable = ['price', 'active']
#    list_filter = ['price', 'active']
 #   readonly_fields = ['updated', 'timestamp']
  #  prepopulated_fields = {"slug": ("title",)}
   # class Meta:
    #    model = Product

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 10

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
    max_num = 10

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price']
    inlines = [ProductImageInline, VariationInline]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
#admin.site.register(Variation)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(ProductFeatured)

import admin_thumbnails
from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter

# Register your models here.
class ProductVariantInlines(admin.TabularInline):
    model = Variatns
    extra = 2


@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model = Images
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name' , 'create' , 'update')
    prepopulated_fields = {
        'slug':('name',)
    }
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name' , 'discount' , 'unit_price' , 'total_price' , 'amount','create')
    list_editable = ('amount',)
    inlines = [ProductVariantInlines,ImageInlines]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user' , 'create' , 'rate']
    list_filter = (
        ('code', JDateFieldListFilter),
    )


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variatns)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Chart)
admin.site.register(Gallery)
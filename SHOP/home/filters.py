import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    CHOISES_1 = {
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    }
    CHOISES_2 = {
        ('قدیمی ترین','قدیمی ترین'),
        ('جدید ترین', 'جدید ترین'),
    }
    CHOISES_3 = {
        ('s','کم فروش'),
        ('پر فروش ترین','پر فروش ترین'),
    }
    CHOISES_4 = {
        ('f','کم محبوب'),
        ('محبوب ترین','محبوب ترین'),
    }
    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    brand = django_filters.ModelMultipleChoiceFilter(queryset= Brand.objects.all(),widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices = CHOISES_1 ,method='price_filter')
    create = django_filters.ChoiceFilter(choices = CHOISES_2,method='create_filter')
    sell = django_filters.ChoiceFilter(choices=CHOISES_3,method='sell_filter')
    favorite = django_filters.ChoiceFilter(choices=CHOISES_4, method='favorite_filter')

    def price_filter(self,queryset,name,value):
        data = 'unit_price' if value == 'ارزان ترین' else '-unit_price'
        return queryset.order_by(data)

    def create_filter(self,queryset,name,value):
        data = 'create' if value == 'قدیمی ترین' else '-create'
        return queryset.order_by(data)

    def sell_filter(self, queryset, name, value):
        data = 'sell' if value == 's' else '-sell'
        return queryset.order_by(data)

    def favorite_filter(self,queryset,name,value):
        data = 'favorite' if value == 'f' else '-favorite'
        return queryset.order_by(data)

from django.db import models
from home.models import *
from django.forms import ModelForm
# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variatns,on_delete=models.CASCADE,null=True,blank=True)
    quantity =models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class Compare(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
        return self.product.name

def ComperForm(ModelForm):
    class Meta:
        model = Compare
        fields = ['product']
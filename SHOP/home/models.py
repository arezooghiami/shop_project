from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.forms import ModelForm
from django.db.models import Avg
from django_jalali.db import models as jmodels
from django.utils import timezone

from django.db.models.signals import post_save

# Create your models here.
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='sub')
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=100,verbose_name='نام دسته بندی')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True,unique=True,null=True,blank=True)
    image = models.ImageField(upload_to='category',null=True,blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category',args=[self.slug,self.id])

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

class Product(models.Model):
    VARIANT =(
        ('None','none'),
        ('Size', 'size'),
        ('Color', 'color'),
    )
    category = models.ManyToManyField(Category,blank=True)
    change = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(null=True,blank=True)
    total_price = models.PositiveIntegerField()
    information = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    brand = models.ForeignKey('Brand',on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(null=True,blank=True,max_length=10,choices=VARIANT)
    tags = TaggableManager(blank=True)
    image = models.ImageField(upload_to='product')
    like = models.ManyToManyField(User, blank=True ,related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.PositiveIntegerField(default=0)
    favorite = models.ManyToManyField(User,blank=True,related_name='fa_user')
    total_favorite = models.IntegerField(default=0)
    sell = models.IntegerField(default=0)
    view = models.ManyToManyField(User, blank=True, null=True, related_name='product_view')
    num_view = models.IntegerField(default=0)



    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    def average(self):
        data = Comment.objects.filter(is_reply=False,product=self).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'],1)
        return star

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


    def get_absolute_url(self):
        return reverse('home:detail',args=[self.id])

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.old_price = self.unit_price

    def save(self,*args,**kwargs):
        if self.old_price != self.unit_price:
            self.update = timezone.now()
        super(Product,self).save(*args,**kwargs)

class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Variatns(models.Model):
    name = models.CharField(max_length=100)
    update = jmodels.jDateTimeField(auto_now=True)
    product_variant = models.ForeignKey(Product,on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE,null=True,blank=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    change = models.BooleanField(default=False)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='comment_reply')
    is_reply = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    comment_like = models.ManyToManyField(User,blank=True,related_name='com_like')
    total_comment_like= models.PositiveIntegerField(default=0)

    def total_comment_like(self):
        return self.comment_like.count()


    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment' , 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to='image/',blank=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chart(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    unit_price = models.IntegerField(default=0)
    update = jmodels.jDateTimeField(auto_now=True)
    color = models.CharField(max_length=50,blank=True,null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pr_update',blank=True,null=True)
    variant = models.ForeignKey(Variatns, on_delete=models.CASCADE, related_name='v_update', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        old_data = Chart.objects.filter(product__exact=self.product,unit_price__exact=self.unit_price)
        if not old_data.exists():
            return super().save(*args,**kwargs)



def product_post_saved(sender,instance,created,*args,**kwargs):
    data = instance
    # if data.change == True :
    Chart.objects.create(product=data,unit_price=data.unit_price,update=data.update,name=data.name)

post_save.connect(product_post_saved,sender=Product)

def variant_post_saved(sender,instance,created,*args,**kwargs):
    data = instance
    if data.change == True :
        Chart.objects.create(variant=data,unit_price=data.unit_price,update=data.update,name=data.name
                             ,size = data.size_variant,color = data.color_variant)

post_save.connect(variant_post_saved,sender=Variatns)


class Views(models.Model):
    ip = models.CharField(max_length=200,null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Gallery(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='gallery/',blank=True)

    def __str__(self):
        return self.name

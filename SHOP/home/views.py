from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import SearchForm
from django.db.models import Q,Min,Max
from cart.models import *
from django.core.paginator import Paginator
from .filters import ProductFilter
from django.http import JsonResponse

# Create your views here.
def home(request):
    category = Category.objects.filter(sub_cat=False)
    gallery = Gallery.objects.all()
    return render(request,'home/home.html',{'category':category,'gallery':gallery})

def all_product(request,slug=None,id=None):
    products = Product.objects.all()
    min = Product.objects.aggregate(unit_price=Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Product.objects.aggregate(unit_price=Max('unit_price'))
    max_price = int(max['unit_price'])
    filter = ProductFilter(request.GET,queryset=products)
    products = filter.qs
    paginator = Paginator(products,5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    form = SearchForm()
    category = Category.objects.filter(sub_cat = False)
    if slug and id:
        data = Category.objects.get(slug=slug,id=id)
        products = products.filter(category=data)
    return render(request,'home/product.html',{'products':page_obj,'category':category,'form':form,'filter':filter,'min_price':min_price,'max_price':max_price})

def product_detail(request,id):
    product = Product.objects.get(id=id)
    ip = request.META.get('REMOTE_ADDR')
    view = Views.objects.filter(product_id=product.id,ip=ip)
    if not view.exists():
        Views.objects.create(product_id=product.id,ip=ip)
        product.num_view += 1
        product.save()
    update = Chart.objects.filter(product_id=id)
    change = Chart.objects.all()
    images = Images.objects.filter(product_id=id)
    cart_form = CartForm()
    similar = product.tags.similar_objects()[:2]
    comment_form = CommentForm()
    reply_form = ReplyForm()
    comment = Comment.objects.filter(product_id=id,is_reply=False,status=True)
    is_like = False
    if product.like.filter(id=request.user.id).exists():
        is_like = True
    is_unlike = False
    if product.unlike.filter(id=request.user.id).exists():
        is_unlike = True

    is_favorite = False
    if product.favorite.filter(id=request.user.id).exists():
        is_favorite = True
    if product.status != 'None':
        if request.method == 'POST':
            variant = Variatns.objects.filter(product_variant_id = id)
            var_id = request.POST.get('select')
            variants = Variatns.objects.get(id=var_id)
        else:
            variant = Variatns.objects.filter(product_variant_id=id)
            variants = Variatns.objects.get(id=variant[0].id)
        context = {'product':product,'variant':variant,'variants':variants,'similar':similar,'is_favorite':is_favorite
            ,'is_like':is_like,'is_unlike':is_unlike,'comment_form':comment_form,'comment':comment,'reply_form':reply_form,'images':images,'cart_form':cart_form,'change':change}
        return render(request,'home/detail.html',context)
    else:
        return render(request,'home/detail.html',{'product':product,'similar':similar,'is_favorite':is_favorite,
                                                  'is_like':is_like,'is_unlike':is_unlike,'comment_form':comment_form,'comment':comment,'reply_form':reply_form,'images':images,'cart_form':cart_form,'update':update})



def product_like(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product,id=id)
    if product.like.filter(id=request.user.id).exists():
        product.like.remove(request.user)
    else:
        product.like.add(request.user)
    return redirect(url)

def product_unlike(request,id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product,id=id)
    if product.unlike.filter(id=request.user.id).exists():
        product.unlike.remove(request.user)
    else:
        product.unlike.add(request.user)
    return redirect(url)

def product_comment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'],rate = data['rate'],user_id = request.user.id,
                                   product_id = id)
    return redirect(url)


def product_reply(request,id,comment_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment=data['comment'],user_id = request.user.id,product_id = id,
                                   reply_id=comment_id,is_reply=True)
    return redirect(url)


def comment_like(request,id):
    url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
    else:
         comment.comment_like.add(request.user)
    return redirect(url)


def product_search(request):
    products = Product.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__exact=data)|Q(unit_price__exact=data))
            else:
                products = products.filter(Q(name__contains=data))
            return  render(request,'home/product.html',{'products':products,'form':form})


def favorite_product(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)

    if product.favorite.filter(id=request.user.id).exists():
        product.favorite.remove(request.user)

        product.total_favorite -=1
        # product.save()
    else:
        product.favorite.add(request.user)
        product.total_favorite += 1
    product.save()
    data ={'success': 'ok'}
    return JsonResponse(data)
    # return redirect(url)

# def product_view(request,id):
#     url = request.META.get('HTTP_REFERER')
#     product = get_object_or_404(Product,id=id)
#     product.view.add(request.user)
#     return redirect(url)
#





from .models import *
from django.db.models import Sum
from cart.models import *

def get_cart(request):
    nums = Cart.objects.filter(user_id=request.user.id).aggregate(sum=Sum('quantity'))['sum']
    context ={'nums':nums}
    return context

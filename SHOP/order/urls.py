from django.urls import path
from . import views
# suds-py3


app_name = 'order'
urlpatterns =[
    path('<int:order_id>/',views.order_detail,name='order_detail'),
    path('create/',views.order_create,name='order_create'),
    path('coupon/<int:order_id>/',views.coupon_order,name='coupon'),
    path('request/<int:price>/<int:order_id>/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
]
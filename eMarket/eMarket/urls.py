"""eMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from carts.views import CartView, ItemCountView, CheckoutView, CheckoutFinalView

from orders.views import AddressSelectFormView, UserAddressCreateView, OrderList, OrderDetail

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^about/$', 'eMarket.views.about', name='about'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^$', 'products.views.home', name='home'),
    #url(r'^products/$', 'products.views.all', name='products'),
    url(r'^products/', include('products.urls')),
    url(r'^categories/', include('products.url_categories')),
    url(r'orders/$',OrderList.as_view(), name="orders"),
    url(r'orders/(?P<pk>\d+)/$',OrderDetail.as_view(), name="order_detail"),
    url(r'cart/$',CartView.as_view(), name="cart"),
    url(r'cart/count/$',ItemCountView.as_view(), name="item_count"),
    url(r'checkout/$', CheckoutView.as_view(), name="checkout"),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

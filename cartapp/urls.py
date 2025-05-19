from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<slug:slug>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/buynow/<slug:slug>/', views.BuyNowView.as_view(), name='buynow_checkout'),
    path('process_payment/',views.ProcessPaymentView.as_view(),name='process_payment'),
    path('checkout/razorpay/',views.RazorpayCheckoutView.as_view(),name='razorpay_checkout'),
    path('razorpay/callback/', views.RazorpayCallbackView.as_view(), name='razorpay_callback'),
]
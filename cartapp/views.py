from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from coreapp.models import ProductVariantModel,ProductModel,PaymentsModel
from authentication.models import Custom_UserModel
from django.contrib import messages
from .models import CartModel,CartItemModel
from orderapp.models import OrderItemModel,OrdersModel,ShippingModel
from django.utils import timezone
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
# Create your views here.
DELIVERY_CHARGE_THRESHOLD = Decimal("499.00")
DELIVERY_CHARGE = Decimal("100.00")
PACKAGING_FEE = Decimal("218.00")


class CartView(View):
    @method_decorator(login_required)
    def get(self, request):
        custom_user = Custom_UserModel.objects.filter(id=request.user.id).first()
        if not custom_user:
            messages.error(request,"You Are Logged In but not as a Valid User. Kindly Register Properly.")
            return redirect('openpage')

        cart,created= CartModel.objects.get_or_create(user=custom_user)

        context = {
            'cart': cart,
            'items': cart.items.all()
        }
        return render(request, 'cartapp/cart.html', context)


class AddToCartView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        custom_user = Custom_UserModel.objects.filter(id=request.user.id).first()
        if not custom_user:
            messages.error(request,"You Are Logged In but not as a Valid User. Kindly Register Properly.")
            return redirect('openpage')

        cart,created= CartModel.objects.get_or_create(user=custom_user)
        selected_size = request.POST.get("selected_size")
        selected_storage = request.POST.get("selected_storage")

        # Pick the one that exists
        selected_option = selected_size or selected_storage

        product_variant = get_object_or_404(ProductVariantModel, slug=kwargs['slug'])
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = CartItemModel.objects.get_or_create(
            cart_id=cart,
            product_variant_id=product_variant,
            defaults={'quantity': quantity,'selected_attribute_value': selected_option}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart')
    
@method_decorator(login_required, name='dispatch')
class UpdateCartItemView(View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItemModel, id=kwargs['item_id'], cart_id__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, f'{cart_item.product_variant_id.product_id.name} updated QUANTITY to {quantity} !!')
        return redirect('cart')

@method_decorator(login_required, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItemModel, id=kwargs['item_id'], cart_id__user=request.user)
        cart_item.delete()
        messages.error(request, f'{cart_item.product_variant_id.product_id.name} removed from cart !!')
        return redirect('cart')

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        custom_user = Custom_UserModel.objects.filter(id=request.user.id).first()
        if not custom_user:
            messages.error(request,"You Are Logged In but not as a Valid User. Kindly Register Properly.")
            return redirect('openpage')
        
        cart = get_object_or_404(CartModel, user=custom_user)
        if not cart.items.exists():
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
            
        context = {
            'cart': cart,
            'items': cart.items.all()
        }
        return render(request, 'cartapp/checkout.html', context)

class ProcessPaymentView(View):
    @method_decorator(login_required)
    def post(self, request):
        custom_user = Custom_UserModel.objects.filter(id=request.user.id).first()
        if not custom_user:
            messages.error(request,"You Are Logged In but not as a Valid User. Kindly Register Properly.")
            return redirect('openpage')
        buy_now_variant_id = request.POST.get("buy_now_variant_id")
        buy_now_quantity = request.POST.get("quantity", 1)

        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        # Case 1: Buy Now flow
        if buy_now_variant_id:
            variant = get_object_or_404(ProductVariantModel, variant_id=buy_now_variant_id)
            quantity = int(buy_now_quantity)
            delivery_charge = Decimal("0.00") if variant.sale_price > DELIVERY_CHARGE_THRESHOLD else DELIVERY_CHARGE
            total_amount = (variant.sale_price * quantity) + PACKAGING_FEE + delivery_charge

            request.session['shipping'] = {
                "name": full_name,
                "address": address,
                "total": float(total_amount),
                "payment_mode": payment_method,
                "buy_now_variant_id": variant.variant_id,
                "quantity": quantity
            }

            if payment_method == "Razorpay":
                return redirect('razorpay_checkout')

            # COD flow
            if payment_method =="COD":
                order_item = OrderItemModel.objects.create(
                    product_id=variant.product_id,
                    quantity=quantity,
                    price=variant.sale_price,
                    ordered=True
                )

                order = OrdersModel.objects.create(
                    user_id=user,
                    total=total_amount,
                    status='Placed (COD)',
                    ordered=True
                )
                order.order_items.add(order_item)

                PaymentsModel.objects.create(
                    order_id=order,
                    user_id=user,
                    amount=total_amount,
                    status="Pending",
                    payment_mode="COD"
                )

                ShippingModel.objects.create(
                    order_id=order,
                    address=address,
                    tracking_id="TRK" + str(timezone.now().timestamp()).replace('.', '')[:15],
                    status="Pending"
                )

                messages.success(request, "Order placed successfully with Cash on Delivery!")
                return redirect('dashboard')

        # Case 2: Cart flow (original logic here)
        cart = CartModel.objects.get(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect('cart')

        total_amount = cart.total_payable

        # Save in session for Razorpay
        if payment_method == "Razorpay":
            request.session['shipping'] = {
                "name": full_name,
                "address": address,
                "total": float(cart.total_payable),
                "payment_mode": payment_method
            }
            return redirect('razorpay_checkout')

    
class BuyNowView(View):
    @method_decorator(login_required)
    def get(self, request, slug):
        variant = get_object_or_404(ProductVariantModel, slug=slug)
        quantity = 1
        original_price = variant.original_price
        sale_price = variant.sale_price

        total_original_price = original_price * quantity
        total_discount = (original_price - sale_price) * quantity
        delivery_charge = Decimal("0.00") if sale_price > DELIVERY_CHARGE_THRESHOLD else DELIVERY_CHARGE
        total_payable = sale_price + delivery_charge + PACKAGING_FEE

        context = {
            'buy_now': True,
            'variant': variant,
            'quantity': quantity,
            'total': sale_price,
            'total_items': quantity,
            'total_original_price': total_original_price,
            'total_discount': total_discount,
            'delivery_charge': delivery_charge,
            'packaging_fee': PACKAGING_FEE,
            'total_payable': total_payable
        }
        return render(request, 'cartapp/buynow_checkout.html', context)

class RazorpayCheckoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        # cart = get_object_or_404(CartModel, user=request.user)
        shipping = request.session.get("shipping")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            "amount": int(shipping['total'] * 100),  # Razorpay uses paise
            "currency": "INR",
            "payment_capture": 1
        })

        context = {
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "order": payment,
            "shipping": shipping
        }
        return render(request, "cartapp/razorpay_payment.html", context)


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayCallbackView(View):
    def post(self, request):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # 1. Get data from frontend (JS handler)
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # 2. Verify Razorpay signature
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failure", "message": "Payment verification failed."}, status=400)

        # 3. Get user + session data
        user = Custom_UserModel.objects.get(id=request.user.id)
        shipping = request.session.get("shipping")

        if not shipping:
            return JsonResponse({"status": "failure", "message": "No shipping info in session."}, status=400)

        is_buy_now = "buy_now_variant_id" in shipping

        order_items = []
        total = Decimal(shipping["total"])
        address = shipping["address"]

        if is_buy_now:
            # 4a. Buy Now
            variant_id = shipping["buy_now_variant_id"]
            quantity = shipping["quantity"]
            variant = get_object_or_404(ProductVariantModel, variant_id=variant_id)

            order_item = OrderItemModel.objects.create(
                product_id=variant.product_id,
                quantity=quantity,
                price=variant.sale_price,
                ordered=True
            )
            order_items.append(order_item)

        else:
            # 4b. Cart flow
            cart = get_object_or_404(CartModel, user=user)
            for item in cart.items.all():
                order_item = OrderItemModel.objects.create(
                    product_id=item.product_variant_id.product_id,
                    quantity=item.quantity,
                    price=item.product_variant_id.sale_price,
                    ordered=True
                )
                order_items.append(order_item)

        # 5. Create Order
        order = OrdersModel.objects.create(
            user_id=user,
            total=total,
            status="Placed (Razorpay)",
            ordered=True
        )
        order.order_items.set(order_items)

        # 6. Create Payment record
        PaymentsModel.objects.create(
            order_id=order,
            user_id=user,
            amount=total,
            status="Paid",
            payment_mode="Razorpay"
        )

        # 7. Create Shipping info
        ShippingModel.objects.create(
            order_id=order,
            address=address,
            tracking_id="TRK" + str(timezone.now().timestamp()).replace('.', '')[:15],
            status="Pending"
        )

        # 8. Cleanup
        if not is_buy_now:
            cart.items.all().delete()

        if 'shipping' in request.session:
            del request.session['shipping']

        return JsonResponse({"status": "success", "message": "Payment successful! Order placed."})

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView
from .models import Item, Order


class ItemDetailView(DetailView):
    model = Item


class OrderDetailView(DetailView):
    model = Order


def create_checkout_session(request, pk):
    if request.method == 'GET':
        try:
            item = Item.objects.get(id=pk)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            domain_url = settings.DOMAIN_NAME
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': item.currency,
                            'unit_amount': item.price,
                            'product_data': {
                                'name': item.name,
                                'description': item.description,
                            }
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=domain_url + '/success/',
                cancel_url=domain_url + '/cancelled/',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def create_checkout_session_order(request, pk):
    if request.method == 'GET':
        try:
            order = Order.objects.get(id=pk)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            domain_url = settings.DOMAIN_NAME

            if order.discount:
                order_discount = stripe.Coupon.create(
                    percent_off=order.discount.percent_off,
                )
            else:
                order_discount = None

            if order.tax:
                order_tax = stripe.TaxRate.create(
                    display_name=order.tax.name,
                    percentage=order.tax.percentage,
                    inclusive=order.tax.inclusive,
                )
                order_tax_id = [order_tax.id]
            else:
                order_tax_id = []

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': order.currency,
                            'unit_amount': order.get_total_cost,
                            'product_data': {
                                'name': order.name,
                                'description': order.description,
                            }
                        },
                        'quantity': 1,
                        'tax_rates': order_tax_id,
                    },
                ],
                mode='payment',
                discounts=[{
                    'coupon': order_discount,
                }],
                success_url=domain_url + '/success/',
                cancel_url=domain_url + '/cancelled/',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def get_stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView
from .models import Item, Order


class ItemDetailView(DetailView):
    """
    Returns HTML page with the information about the selected item (passed by id)
    and the 'Buy' button.
    """
    model = Item


class OrderDetailView(DetailView):
    """
    Returns HTML page with the information about the selected order (passed by id)
    and the 'Buy' button.
    """
    model = Order


def create_checkout_session(request, pk):
    """
    Returns json with Stripe API (https://stripe.com/docs/api) checkout session id
    for product or error if something went wrong.
    """
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
    """
    Returns json with Stripe API (https://stripe.com/docs/api) checkout session id
    for order or error if something went wrong.
    """
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
    """
    Returns json with Stripe API public key.
    """
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class SuccessView(TemplateView):
    """Generates a page where users are redirected after
    successful payment."""
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    """Generates a page where users are redirected after
    failed payment."""
    template_name = 'payments/cancelled.html'

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
                            'currency': 'usd',
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
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': order.get_total_cost,
                            'product_data': {
                                'name': order.name,
                                'description': order.description,
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




def get_stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'






"""
stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        item = Item.objects.get(name="Table")
        context = super().get_context_data(**kwargs)
        context.update({
            "item": item
        })
        return context


class CreateCheckoutSession(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)

        YOUR_DOMAIN = 'http://localhost:8000'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancelled/',
        )
        return JsonResponse({'id': checkout_session.id})



class HomePageView(TemplateView):
    template_name = 'home.html'





@csrf_exempt
def get_stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 100,
                        'product_data': {
                            'name': 'T-shirt',
                            'description': 'A BOOK!!!',
                        },
                    },
                    'quantity': 1,
                }],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")

    return HttpResponse(status=200)
"""


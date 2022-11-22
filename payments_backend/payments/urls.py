from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HomePageView.as_view(), name='home'),
    # path('create-checkout-session/', views.create_checkout_session),
    # # path('webhook/', views.stripe_webhook),
    # path('create-checkout-session/<pk>/', views.CreateCheckoutSession.as_view(),
    #      name='create-checkout-session'),
    # path('', views.ProductLandingPageView.as_view(), name='landing-page'),
    path('config/', views.get_stripe_config, name='config'),
    path('item/<pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('buy/<pk>/', views.create_checkout_session, name='create-checkout-session'),
    path('order/<pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('buy/order/<pk>', views.create_checkout_session_order,
         name='create-checkout-session-order'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
]

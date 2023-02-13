from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.get_stripe_config, name='config'),
    path('item/<pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('buy/<pk>/', views.create_checkout_session, name='create-checkout-session'),
    path('order/<pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('buy/order/<pk>/', views.create_checkout_session_order,
         name='create-checkout-session-order'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
]

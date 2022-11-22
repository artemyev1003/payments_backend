from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HomePageView.as_view(), name='home'),
    # path('create-checkout-session/', views.create_checkout_session),
    # path('success/', views.SuccessView.as_view(), name='success'),
    # path('cancelled/', views.CancelledView.as_view(), name='cancelled'),
    # # path('webhook/', views.stripe_webhook),
    # path('create-checkout-session/<pk>/', views.CreateCheckoutSession.as_view(),
    #      name='create-checkout-session'),
    # path('', views.ProductLandingPageView.as_view(), name='landing-page'),
    path('config/', views.get_stripe_config, name='config'),
    path('item/<pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('buy/<pk>/', views.create_checkout_session, name='create-checkout-session'),
]

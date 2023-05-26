from django.urls import path
from . import views


app_name  = 'payment'
urlpatterns = [
  
  path('booking-history/',views.booking_history,name='booking-history'),
  path('booking-history-detail/<str:uid>/',views.booking_history_detail,name='booking_history_detail'),
  path('checkout-session/<str:uid>/',views.create_stripe_checkout_session,name='checkout-session'),
  path('success/',views.SuccessView.as_view(),name='success'),
  path('cancel/',views.CancelView.as_view(),name='cancel'),
  path('webhook/',views.StripeWebhookView.as_view(),name='webhook'),
  

]

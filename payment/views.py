from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.views.generic import View,TemplateView
from home.models import *
from .models import *
import stripe
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import datetime
from django.shortcuts import render
from payment.models import HotelBookingHistory
from home.models import HotelImages

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_checkout_session(request, uid):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    try:
        booking_obj = BookingDetail.objects.get(uid=uid)
    except BookingDetail.DoesNotExist:
        raise Http404("BookingDetail matching query does not exist.")

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        invoice_creation={
            "enabled": True,
            "invoice_data": {
            "description": "Invoice for Product X",
            "metadata": {"order": "order-xyz"},
            # "account_tax_ids": ["DE123456789"],
            "custom_fields": [{"name": "Purchase Order", "value": "PO-XYZ"}],
            "rendering_options": {"amount_tax_display": "include_inclusive_tax"},
            "footer": "B2B Inc.",
            },
        },
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "unit_amount": int(booking_obj.total_amount) * 100,
                    "product_data": {
                        "name": booking_obj.hotel,
                    },
                },
                "quantity":1,
            }
        ],
        metadata={"product_id": booking_obj.uid},
        mode="payment",
        success_url=settings.PAYMENT_SUCCESS_URL,
        cancel_url=settings.PAYMENT_CANCEL_URL,
    )
    return redirect(checkout_session.url)


    
class SuccessView(TemplateView):
    template_name = "success.html"    


class CancelView(TemplateView):
    template_name = "cancel.html"

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """
    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            # print(event)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")

            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            customer_name=session["customer_details"]["name"]
            product_id = session["metadata"]["product_id"]
            product = get_object_or_404(BookingDetail, uid=product_id)
            
        
            payment_intent = stripe.PaymentIntent.retrieve(session["payment_intent"])
            balance_transaction = payment_intent["charges"]["data"][0]["balance_transaction"]
            print("transaction_id :",balance_transaction)

        
            message = f"Dear {customer_name},\n\nThank you for booking with us.\n\nHere are your booking details:\n\nBooking ID: {product.uid}\nCustomer Name: {customer_name}\nCheck-In Date: {product.start_date}\nCheck-Out Date: {product.end_date}\nTotal Amount: {product.total_amount}\n\nThank you for choosing our hotel. We look forward to hosting you.\n\nBest regards,\nThe Motelo Hotel Team !"
            send_mail(
                subject='Booking Details',
                message=message,
                from_email='noreply@hotel.com',
                recipient_list=[customer_email],
                fail_silently=False,
            )
            customer = stripe.Customer.create(
                name=customer_name,
                email=customer_email,
                source="tok_visa" # replace this with the actual payment source
            )
            due_date_str = product.end_date.strftime('%Y-%m-%d')
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d')
            due_timestamp = int(due_date.timestamp())
            # get the customer ID
            customer_id = customer.id          
            invoice = stripe.Invoice.create(
                customer=customer_id,
                description="Booking invoice",
                currency="inr",
                collection_method = 'send_invoice',
                due_date= due_timestamp
                # transaction_id=balance_transaction
            )
            
            inv = stripe.Invoice.retrieve(invoice.id)
            inv_url = inv.hosted_invoice_url
            print("invoice id : ",invoice.id)
            print("invoice url : ",inv_url)
            HotelBookingHistory.objects.create(
                booking_data=product,
                email=customer_email,
                booking_status="booked",
                payment_intent_id=session.get("payment_intent"),
                transaction_id=balance_transaction,
                amount=product.total_amount,
                invoice_id=invoice.id,
                invoice_url=invoice.hosted_invoice_url
            )
            print("history data saved ")
            invoice.send_invoice()
            print(invoice.invoice_pdf)
        
        # Can handle other events here.

        return HttpResponse(status=200)
    
class StripeRefundView(View):
    """
    StripeRefundView is the API of refund resource, and
    responsible to handle the requests of /refund/ endpoint.
    """
    def post(self, request, format=None):
        p_id = HotelBookingHistory.objects.filter(id=id)
        payment_intent=stripe.PaymentIntent.retrieve(p_id)
        refund = stripe.Refund.create(p_id)
        return HttpResponse(refund,"Payment Refunded!!")
    

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookRefundView(View):

    """
    Stripe webhook view to handle checkout session completed and refund events.

    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "payment_intent.refund.created":
            print("Refund created")
            session = event["data"]["object"]
            refund = event["data"]["object"]
            payment_intent_id = refund["payment_intent"]
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            customer_email = payment_intent["charges"]["data"][0]["billing_details"]["email"]
            product_id = payment_intent["metadata"]["product_id"]
            product = get_object_or_404(BookingDetail, uid=product_id)

            balance_transaction = payment_intent["charges"]["data"][0]["balance_transaction"]

            send_mail(
                subject="Refund initiated",
                message=f"Thanks for Booking.Your room is: {product.alloted_rooms} \n  Your transaction id is {balance_transaction}",
                recipient_list=[customer_email],
                from_email="your@email.com",
            )
            if "subscription" in session:
                invoice = stripe.Invoice.retrieve(session["subscription"])
                invoice_id = invoice["id"]
                invoice_url = invoice["hosted_invoice_url"]
            else:
                # Handle the case when there is no subscription ID in the session object
                invoice_id = None
                invoice_url = None
            invoice = stripe.Invoice.create(
                customer=customer_email,
                description="Booking invoice",
                amount=product.total_amount,
                currency="usd",
                transaction_id=balance_transaction
            )

# Send the invoice to the customer's email
            invoice.send_invoice()
            HotelBookingHistory.objects.create(
                booking_data=product,
                email=customer_email,
                booking_status="refunded",
                payment_intent_id=payment_intent_id,
                transaction_id=balance_transaction,
                amount=product.total_amount,
                invoice_id=invoice_id,
                invoice_url=invoice_url
            )


        return HttpResponse(status=200)
    


def booking_history(request):
    user=request.user
    data=HotelBookingHistory.objects.filter(booking_data__user=user) 
    return render(request,'booking_history.html',{"data":data})

def booking_history_detail(request,uid):
    user=request.user
    data=HotelBookingHistory.objects.filter(uid=uid) 
    return render(request,'booking_history_detail.html',{"booking":data,'user':user})


# Generated by Django 4.1.7 on 2023-05-05 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingDetail",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now_add=True)),
                ("hotel", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("total_days", models.IntegerField()),
                ("total_room", models.IntegerField()),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
                ),
                (
                    "alloted_rooms",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="HotelBookingHistory",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now_add=True)),
                ("email", models.EmailField(max_length=254)),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, default=1.0, max_digits=10),
                ),
                (
                    "booking_status",
                    models.CharField(
                        choices=[
                            ("P", "pending"),
                            ("B", "booked"),
                            ("F", "failed"),
                            ("R", "refunded"),
                        ],
                        default="pending",
                        max_length=2,
                    ),
                ),
                (
                    "payment_intent_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("invoice_id", models.CharField(blank=True, max_length=50, null=True)),
                ("invoice_url", models.URLField(blank=True, null=True)),
                (
                    "booking_data",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="booking_detail",
                        to="payment.bookingdetail",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
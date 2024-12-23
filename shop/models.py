from datetime import timedelta

from django.db import models
from django.db.models import DateField, ExpressionWrapper, F
from django.db.models.functions import TruncMonth, Coalesce, Cast
from django.utils import timezone


class RangedModelManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                effective_start_date=TruncMonth("start_date", output_field=DateField()),
                effective_end_date=ExpressionWrapper(
                    TruncMonth(
                        ExpressionWrapper(
                            TruncMonth(
                                Coalesce(
                                    F("end_date"), Cast(timezone.now(), DateField())
                                )
                            )
                            + timedelta(days=32),
                            output_field=DateField(),
                        )
                    )
                    - timedelta(days=1),
                    output_field=DateField(),
                ),
            )
        )


class RangedModel(models.Model):
    class Meta:
        abstract = True

    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True, blank=True, default=None)
    effective_start_date = None
    effective_end_date = None

    objects = RangedModelManager()


class RentTypes(models.TextChoices):
    SHOP = "SHOP", "Shop"
    STORAGE = "STORAGE", "Storage"


class RentCost(RangedModel):
    key = models.CharField(max_length=10, choices=RentTypes)
    cost = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return f"{self.key.capitalize()} @ ${self.cost} from {self.effective_start_date} to {self.effective_end_date}"


class Renter(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return self.name


class RenterRange(RangedModel):
    renter = models.ForeignKey(to="shop.Renter", on_delete=models.CASCADE)
    access = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self):
        return f"{self.renter.name} from {self.effective_start_date} to {self.effective_end_date}"


class Bike(models.Model):
    owner = models.ForeignKey(to="shop.Renter", on_delete=models.CASCADE)
    description = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return f"{self.owner.name}: {self.description}"


class StorageRange(RangedModel):
    bike = models.ForeignKey(to="shop.Bike", on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.bike.owner}'s {self.bike.description} "
            f"from {self.effective_start_date} to {self.effective_end_date}"
        )


class RentPaidManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                effective_date_paid=TruncMonth("date_paid", output_field=DateField()),
            )
        )


class RentPaid(models.Model):
    date_paid = models.DateField(null=False)
    renter = models.ForeignKey(to="shop.Renter", on_delete=models.CASCADE)
    amount_paid = models.IntegerField(default=0, null=False, blank=False)
    effective_date_paid = None

    objects = RentPaidManager()

    def __str__(self):
        return (
            f"{self.renter.name} paid ${self.amount_paid} on {self.effective_date_paid}"
        )

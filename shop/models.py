from datetime import timedelta, datetime

from django.db import models
from django.db.models import DateField, ExpressionWrapper, F, Q
from django.db.models.functions import TruncMonth, Coalesce, Cast
from django.utils import timezone


class RangedModelManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                effective_start_date=TruncMonth("start_date", output_field=DateField()),
                effective_end_date=TruncMonth(
                    ExpressionWrapper(
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
    RENT = "RENT", "Rent"
    SHOP = "SHOP", "Shop"
    STORAGE = "STORAGE", "Storage"


class RentCost(RangedModel):
    key = models.CharField(max_length=10, choices=RentTypes)
    cost = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        verbose_name = "Rent Cost"
        verbose_name_plural = "Rent Cost"

    def __str__(self):
        end = "to " + str(self.end_date) if self.end_date else ""
        return f"{self.key.capitalize()} @ ${self.cost} from {self.effective_start_date} {end}"


class Renter(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return self.name


class RenterRange(RangedModel):
    renter = models.ForeignKey(to="shop.Renter", on_delete=models.CASCADE)
    access = models.BooleanField(null=False, blank=False, default=True)
    bikes = None

    class Meta:
        verbose_name = "Renter Range"
        verbose_name_plural = "Renter Ranges"

    def __str__(self):
        end = "to " + str(self.end_date) if self.end_date else ""
        return f"{self.renter.name} from {self.effective_start_date} {end}"


class Bike(models.Model):
    owner = models.ForeignKey(
        to="shop.Renter", on_delete=models.CASCADE, related_name="bikes"
    )
    description = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return f"{self.owner.name}: {self.description}"


class StorageRange(RangedModel):
    bike = models.ForeignKey(to="shop.Bike", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Storage Range"
        verbose_name_plural = "Storage Ranges"

    def __str__(self):
        end = "to " + str(self.end_date) if self.end_date else ""
        return (
            f"{self.bike.owner}'s {self.bike.description} "
            f"from {self.effective_start_date} {end}"
        )

    def save(self, **kwargs):
        existing_records = StorageRange.objects.filter(bike=self.bike).filter(
            Q(effective_start_date__lte=self.end_date or datetime.now())
            & Q(effective_end_date__gte=self.start_date)
        )

        if not self._state.adding:
            existing_records = existing_records.exclude(id=self.id)

        if existing_records.exists():
            raise ValueError(
                "That range overlaps with an existing storage range for that bike"
            )

        super().save(**kwargs)


class RentPaidManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                effective_date_paid=TruncMonth("date_paid", output_field=DateField()),
            )
            .order_by("date_paid")
        )


class RentPaid(models.Model):
    date_paid = models.DateField(null=False)
    renter = models.ForeignKey(to="shop.Renter", on_delete=models.CASCADE)
    amount_paid = models.IntegerField(default=0, null=False, blank=False)
    effective_date_paid = None

    objects = RentPaidManager()

    class Meta:
        verbose_name = "Rent Paid"
        verbose_name_plural = "Rent Paid"

    def __str__(self):
        return f"{self.renter.name} paid ${self.amount_paid} on {self.date_paid}"

import datetime
import itertools

from dateutil.rrule import rrule, MONTHLY
from django.http import HttpResponse
from django.template import loader

from shop.models import RenterRange, RentCost, RentTypes, RentPaid


def rent_due(request):
    template = loader.get_template("shop/rent_due.html")

    search_start = datetime.date(2023, 1, 1)
    search_end = datetime.datetime.now()

    renter_range_for_range = list(
        RenterRange.objects.filter(
            effective_start_date__lte=search_end, effective_end_date__gte=search_start
        ).order_by("effective_start_date", "renter__name")
    )

    visible_dates = [
        date.date() for date in rrule(MONTHLY, dtstart=search_start, until=search_end)
    ]

    ###############################################################
    # Shop Rent Costs

    shop_rent_cost_records = list(
        RentCost.objects.filter(
            key=RentTypes.SHOP,
            effective_start_date__lte=search_end,
            effective_end_date__gte=search_start,
        )
    )

    shop_rent_cost_by_date = {
        this_date: sum(
            rate.cost
            for rate in shop_rent_cost_records
            if rate.effective_start_date <= this_date <= rate.effective_end_date
        )
        for this_date in visible_dates
    }

    ###############################################################
    # Storage Rent Costs

    storage_rent_cost_records = list(
        RentCost.objects.filter(
            key=RentTypes.STORAGE,
            effective_start_date__lte=search_end,
            effective_end_date__gte=search_start,
        )
    )

    storage_rent_cost_by_date = {
        this_date: sum(
            rate.cost
            for rate in storage_rent_cost_records
            if rate.effective_start_date <= this_date <= rate.effective_end_date
        )
        for this_date in visible_dates
    }

    ###############################################################
    # Rent Paid

    rent_paid_records = {
        date_paid: list(rents_paid)
        for date_paid, rents_paid in itertools.groupby(
            RentPaid.objects.filter(
                date_paid__gte=search_start, date_paid__lte=search_end
            ),
            lambda x: x.effective_date_paid,
        )
    }

    rents_paid = {
        this_date: {
            renter: sum(rp.amount_paid for rp in rent_paid)
            for renter, rent_paid in itertools.groupby(
                rent_paid_records.get(this_date, []), lambda x: x.renter
            )
        }
        for this_date in visible_dates
    }

    ###############################################################
    # Merge it all

    calendar_contents = {
        this_date: [
            {
                "renter": renter_range.renter,
                "storage": storage_rent_cost_by_date[this_date],
                "shop": shop_rent_cost_by_date[this_date] if renter_range.access else 0,
                "total": (
                    (shop_rent_cost_by_date[this_date] if renter_range.access else 0)
                    + storage_rent_cost_by_date[this_date]
                ),
                "paid": (rents_paid[this_date].get(renter_range.renter, 0)),
            }
            for renter_range in renter_range_for_range
            if (
                renter_range.effective_start_date
                <= this_date
                <= renter_range.effective_end_date
            )
        ]
        for this_date in visible_dates
    }

    context = {
        "visible_dates": visible_dates,
        "calendar_contents": calendar_contents,
    }

    return HttpResponse(template.render(context, request))

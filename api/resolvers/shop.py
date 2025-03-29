import datetime
import itertools

from ariadne import QueryType
from dateutil.rrule import rrule, MONTHLY

from shop.models import Renter, StorageRange
from shop.models import RenterRange, RentCost, RentTypes, RentPaid

query = QueryType()


@query.field("renter")
def resolve_renter(*_, renter_id):
    renter = Renter.objects.filter(id=renter_id)
    assert renter.exists(), "Renter must've been instantiated"
    return renter.get()


@query.field("renters")
def resolve_renters(*_):
    return Renter.objects.all()


@query.field("rentStats")
def rent_due(*_):
    search_end = datetime.datetime.now()
    search_start = (search_end - datetime.timedelta(days=365)).replace(day=1)

    renter_range_for_range = list(
        RenterRange.objects.filter(
            effective_start_date__lte=search_end, effective_end_date__gte=search_start
        )
    )

    visible_dates = [
        date.date() for date in rrule(MONTHLY, dtstart=search_start, until=search_end)
    ]

    visible_dates.reverse()

    ###############################################################
    # Shop Rent Costs

    shop_rent_cost_records = list(
        RentCost.objects.filter(
            key=RentTypes.RENT,
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
    # Shop Access Costs

    shop_access_cost_records = list(
        RentCost.objects.filter(
            key=RentTypes.SHOP,
            effective_start_date__lte=search_end,
            effective_end_date__gte=search_start,
        )
    )

    shop_access_cost_by_date = {
        this_date: sum(
            rate.cost
            for rate in shop_access_cost_records
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

    # for this_date in visible_dates:
    #     Renter.objects.annotate(bike_count=Count("storage_range__"))
    #     storage = StorageRange.objects.filter(
    #         effective_start_date__lte=this_date, effective_end_date__gte=this_date
    #     )

    # storage_rent_owed_by_date = {
    #     this_date: {
    #         storage.bike.owner: storage
    #         for storage in StorageRange.objects.filter(
    #             effective_start_date__lte=this_date, effective_end_date__gte=this_date
    #         ).all()
    #     }
    #     for this_date in visible_dates
    # }

    ###############################################################
    # Rent Paid

    rent_paid_records = {
        date_paid: list(rents_paid)
        for date_paid, rents_paid in itertools.groupby(
            RentPaid.objects.filter(
                effective_date_paid__gte=search_start,
                effective_date_paid__lte=search_end,
            ),
            lambda x: x.effective_date_paid,
        )
    }

    rents_paid_by_date = {
        this_date: {
            renter: sum(rp.amount_paid for rp in rent_paid)
            for renter, rent_paid in itertools.groupby(
                rent_paid_records.get(this_date, []), lambda x: x.renter
            )
        }
        for this_date in visible_dates
    }

    def bike_count(this_date, renter):
        x = StorageRange.objects.filter(
            effective_start_date__lte=this_date,
            effective_end_date__gte=this_date,
            bike__owner=renter,
        )
        return x.count()

    calendar_contents = [
        {
            "date": this_date,
            "rent": shop_rent_cost_by_date[this_date],
            "values": [
                {
                    "renter": renter_range.renter,
                    "bikes": bike_count(this_date, renter_range.renter),
                    "storage": storage_rent_cost_by_date[this_date]
                    * bike_count(this_date, renter_range.renter),
                    "access": renter_range.access,
                    "shop": (
                        shop_access_cost_by_date[this_date]
                        if renter_range.access
                        else 0
                    ),
                    "paid": (rents_paid_by_date[this_date].get(renter_range.renter, 0)),
                }
                for renter_range in renter_range_for_range
                if (
                    renter_range.effective_start_date
                    <= this_date
                    <= renter_range.effective_end_date
                )
            ],
        }
        for this_date in visible_dates
    ]

    return {
        "visible_dates": visible_dates,
        "calendar_contents": calendar_contents,
    }

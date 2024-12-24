from django.contrib import admin

from shop.models import Renter, Bike, RenterRange, StorageRange, RentCost, RentPaid


class RentCostAdmin(admin.ModelAdmin):
    pass


admin.site.register(RentCost, RentCostAdmin)


class RenterAdmin(admin.ModelAdmin):
    ordering = ("name",)


admin.site.register(Renter, RenterAdmin)


class RenterRangeAdmin(admin.ModelAdmin):
    ordering = ("start_date", "renter__name")


admin.site.register(RenterRange, RenterRangeAdmin)


class BikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bike, BikeAdmin)


class StorageRangeAdmin(admin.ModelAdmin):
    pass


admin.site.register(StorageRange, StorageRangeAdmin)


class RentPaidAdmin(admin.ModelAdmin):
    ordering = ("-id",)


admin.site.register(RentPaid, RentPaidAdmin)

from django.contrib import admin
from .models import Reservation,Customer,Room,ContactMessage

class ReservationAdmin(admin.ModelAdmin):
    readonly_fields=("created","updated")




# Register your models here.
admin.site.register(Reservation,ReservationAdmin)
admin.site.register(Customer)
admin.site.register(Room)
admin.site.register(ContactMessage)
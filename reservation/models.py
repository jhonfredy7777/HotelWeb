from django.db import models
from django.contrib.auth.models import User
from user.models import Customer


# Create your models here.


class Room(models.Model):
    CATEGORY_CHOICES = [
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    ]

    number = models.PositiveIntegerField(unique=True)  # unique and positive numbers
    category = models.CharField( choices=CATEGORY_CHOICES, default='standard', max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    beds = models.PositiveIntegerField(default=1)  
    available = models.BooleanField(default=True)

    #images
    livingroom = models.ImageField(upload_to='rooms/livingroom/', blank=True, null=True)
    kitchen = models.ImageField(upload_to='rooms/kitchen/', blank=True, null=True)
    bathroom = models.ImageField(upload_to='rooms/bathroom/', blank=True, null=True)
    bedroom = models.ImageField(upload_to='rooms/bedroom/', blank=True, null=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        status = "Available" if self.available else "Occupied"
        return f"Room {self.number} - {self.get_category_display()} ({status}, {self.beds} beds)"



class Reservation(models.Model):
    room=models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    time = models.TimeField()
    state = models.CharField(max_length=100, choices=[("Pending", "Pending"), ("Confirmed", "Confirmed")])
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=[('active', 'Active'), ('cancelled', 'Cancelled')], default='active')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    res_code = models.CharField(max_length=20, unique=True, blank=True,editable=False)
    res_email=models.EmailField(blank=True, null=True)
    behalf_of=models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        ordering = ['-created']

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
    
    def save(self, *args, **kwargs):
        if not self.res_code:
            last = Reservation.objects.all().order_by('id').last()
            next_id = last.id + 1 if last else 1
            self.res_code = f"RES-{next_id:04d}"  # RES-0001, RES-0002...
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Reservation {self.res_code} by {self.customer.full_name}: room-{self.room.number} the {self.date} at {self.time}"
    

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.full_name} - {self.subject}"

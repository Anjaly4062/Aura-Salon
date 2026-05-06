
from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )
    username = models.CharField(max_length=100,null=True)
    email = models.EmailField(unique=True,null=True)  
    password = models.CharField(max_length=100,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Service(models.Model):
   
    service_name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.service_name

class StaffService(models.Model):
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'staff'}
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.staff} - {self.service}"


class Booking(models.Model):
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'staff'},
        related_name="staff_bookings",
        null=True,
        blank=True
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True)  

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.customer} - {self.service}"
    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service_type = models.CharField(max_length=100)
    experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
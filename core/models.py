# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    ROLE_CHOICES = [
        ("Owner", "Owner"),
        ("Tenant", "Tenant"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Property(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Occupied", "Occupied"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    address = models.TextField()

    rent = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bedrooms = models.PositiveIntegerField()

    bathrooms = models.PositiveIntegerField()

    description = models.TextField()

    image = models.ImageField(
        upload_to="property_images/",
        blank=True,
        null=True
    )
    views = models.PositiveIntegerField(
    default=0
)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
class Inquiry(models.Model):

    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.tenant.username} -> {self.property.title}"
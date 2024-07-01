from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    library_card_no = models.IntegerField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    membership_date = models.DateField(auto_now_add=True)
    books_issued = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Added balance field


    def __str__(self):
        return str(self.library_card_no)

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.email)

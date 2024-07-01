from django.db import models
from app_users.models import UserLibraryAccount
from library.models import Book

# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserLibraryAccount, related_name = 'transactions', on_delete = models.CASCADE) # ekjon user er multiple transactions hote pare
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    timestamp = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    is_book_transaction = models.BooleanField(default=False)  # New field to differentiate book transactions
    class Meta:
        ordering = ['timestamp'] 
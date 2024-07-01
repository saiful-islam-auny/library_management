from django.db import models

# Create your models here.
from category.models import Category
from django.contrib.auth.models import User



# Create your models here.
class Book(models.Model):
    category = models.ManyToManyField(Category) # ekta post multiple categorir moddhe thakte pare abar ekta categorir moddhe multiple post thakte pare
    title = models.CharField(max_length=50)
    description= models.TextField()
    # category = models.ManyToManyField(Category) # ekta post multiple categorir moddhe thakte pare abar ekta categorir moddhe multiple post thakte pare
    borrowing_price= models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='library/media/uploads/',blank=True,null=True)
    borrow_book = models.BooleanField(default=False)
    def __str__(self):
        return self.title 
    

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) # jkhn e ei class er object toiri hobe sei time ta rekhe dibe
    
    def __str__(self):
        return f"Comments by {self.name}"
    
from django.db import models
from django.contrib.auth.models import User

class Management(models.Model):
    BookRating=models.FloatField(max_length=50)
    cover_image = models.ImageField(upload_to='static/Userview/',default='')
    BookAuthor=models.CharField(max_length=100)
    Booktitle=models.TextField(default='')
    Bookprice=models.FloatField(default=1.0)

    def __str__(self):
        return self.Booktitle


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    book = models.ForeignKey(Management, on_delete=models.CASCADE , default=1)

    quantity = models.PositiveIntegerField(default=1)
    def total_price(self):
        return self.book.Bookprice * self.quantity
    
    def __str__(self):
        return self.user.username


from django.db import models
from account import models as account_model
from books import models as books_model
from datetime import datetime

class Goal(models.Model):
    UID = models.ForeignKey(account_model.Account,on_delete=models.CASCADE)
    year = models.IntegerField(default=datetime.now().year)
    month = models.IntegerField(default=datetime.now().month)
    numBooks = models.PositiveIntegerField()
    numFinished = models.IntegerField(default=0) 
    books = models.ManyToManyField(books_model.Books)

    class Meta:
        unique_together = (('UID', 'year','month'),)
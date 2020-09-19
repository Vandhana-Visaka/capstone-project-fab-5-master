from django.db import models
from account.models import Account
from books.models import Books
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    '''
    Review Model consists of UID and BID to connect books ans user to review
    rating allows users to rate the book from one to five
    review allows text summary
    '''
    UID = models.ForeignKey(Account,on_delete=models.DO_NOTHING)
    BID = models.ForeignKey(Books,on_delete=models.DO_NOTHING)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    review = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review

    class Meta:
        verbose_name = "Reviews"
        verbose_name_plural = "Reviews"

from django.db import models
from account import models as account_model
from books import models as books_model

class Collection(models.Model):
    '''
    Collection is a group of books under a name/category
    Consists of Book ID and User ID
    Has a collection ID that is unique
    '''
    UID = models.ForeignKey(account_model.Account,on_delete=models.DO_NOTHING)
    collectionName = models.CharField(max_length=100)
    description = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True) 
    books = models.ManyToManyField(books_model.Books,through='Booksadd')

    def __str__(self):
        return self.collectionName

    def get_collection_item(self):
        return self.id

    def get_UID(self):
        return self.UID

    class Meta:
        verbose_name = "Collections"
        verbose_name_plural = "Collections"



class Booksadd(models.Model):
    '''
    Intermediate model for collections to record each add books extra attributes like added_date
    Foreign Keys are used to provide Many to Many Relationship
    '''
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    book = models.ForeignKey(books_model.Books, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    

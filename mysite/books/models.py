from django.db import models
from django.shortcuts import reverse

class Books(models.Model):
    '''
    Books model creates a schema to store the class Book with instances to desribe it.
    Books is characterised by ISBN,title,authors, genres, summary,language, country,etc
    returns self
    '''
    ISBN = models.CharField(max_length=50,unique=True,primary_key=True)
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=500,default="")
    genres = models.CharField(max_length=500,default="")
    summary = models.TextField(blank=True)
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    num_page = models.IntegerField()
    cover = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    publisher = models.CharField(max_length=200)
    publication_date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['-ISBN']

    def __str__(self):
        return self.ISBN

    def get_add_to_collection_isbn(self):
        return self


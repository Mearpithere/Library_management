from django.db import models

# Create your models here.

class Author(models.Model):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(null=True)
    birth_year=models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=300,null=True)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    
    def __str__(self):
        return self.title
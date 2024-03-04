from django.db import models

# Create your models here.



class Students(models.Model):
    name = models.CharField(max_length = 100)
    age  = models.IntegerField(default = 18)
    father_name= models.CharField(max_length=100)

class Category(models.Model):
    categoryName = models.CharField(max_length = 100)
    
class Book(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    bookTitle= models.CharField(max_length = 100)
    
    
    
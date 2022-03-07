from django.db import models
from django.utils.timezone import now

class Listing(models.Model):
   class SaleType(models.TextChoices):
      FOR_SALE = 'for sale'
      FOR_RENT = 'for rent'
   
   class HomeType(models.TextChoices):
      HOUSE = 'house'
      CONDO = 'condo'
      TOWNHOUSE = 'town house'

   # we can't have foreign key relation btn user and listing as we have 2 separated databases
   realtor = models.EmailField(max_length=255)
   title = models.CharField(max_length=255)
   slug = models.SlugField(unique=True)
   address = models.CharField(max_length=255)
   city = models.CharField(max_length=255)
   state = models.CharField(max_length=255)
   zipcode = models.CharField(max_length=30)
   description = models.TextField()
   price = models.IntegerField()
   bedrooms = models.IntegerField()
   bathrooms = models.DecimalField(max_digits=2, decimal_places=1, default=1.0) 
   sale_type = models.CharField(max_length=15, choices=SaleType.choices, default=SaleType.FOR_SALE)
   home_type = models.CharField(max_length=15, choices=HomeType.choices, default=HomeType.HOUSE)
   main_photo = models.ImageField(upload_to='listings/')
   photo_1 = models.ImageField(upload_to='listings/')
   photo_2 = models.ImageField(upload_to='listings/')
   photo_3 = models.ImageField(upload_to='listings/')
   is_published = models.BooleanField(default=False)
   date_created = models.DateTimeField(default=now)

   def __str__(self):
      return self.title
from rest_framework import serializers
from . import models

class ListingSerializer(serializers.ModelSerializer):
   class Meta:
      model=models.Listing
      fields='__all__'
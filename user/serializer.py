from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model=User
      # we need to serialize the name, email, and we need to know if its realtor or not
      fields = ('name', 'email', 'is_realtor',)

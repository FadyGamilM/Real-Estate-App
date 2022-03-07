from django.db import models

from django.contrib.auth.models import (
   AbstractBaseUser,
   BaseUserManager,
   PermissionsMixin
)

class UserAccountManager(BaseUserManager):
   def create_user(self, email, name, password=None):
      """create normal users"""
      if not email:
         raise ValueError("User must has an email address to register")
      email = self.normalize_email(email)
      email = email.lower()
      user=self.model(email=email, name=name)
      user.set_password(password)
      user.is_superuser = False
      # as we are dealing with multiple databases, we have to set the field using 
      user.save(using=self._db)
      return user
   
   def create_realtor(self, email, name, password=None):
      """create realtor users"""
      user = self.create_user(email=email, name=name, password=password)
      user.is_realtor=True
      user.save(using=self._db)
      return user
   
   def create_superuser(self, email, name, password=None):
      """Create a super user who can control the both DBs"""
      user=self.create_user(email, name, password)
      # give this user the admin permissions
      user.is_superuser=True
      # make this user log to the admin pannel
      user.is_staff=True
      user.save(using=self._db)
      return user
   
class UserAccount(AbstractBaseUser, PermissionsMixin):
   email=models.EmailField(max_length=200, unique=True)
   name=models.CharField(max_length=50)
   # while we don't have a mail activation feature, so we will set is_active to True
   is_active=models.BooleanField(default=True)
   is_staff=models.BooleanField(default=False)
   # we have 2 type sof users, normal and realtor
   is_realtor=models.BooleanField(default=False)
   objects=UserAccountManager()
   USERNAME_FIELD='email'
   REQUIRED_FIELDS=['name']
   def __str__(self):
      return self.email


class AuthRouter:
   # pass your app name to the following field
   route_app_labels = {'user', 'admin', 'contenttypes', 'sessions',}

   def db_for_read(self, model, **hints):
      """make attempts to read from our user model go to our user database"""
      # Lets check that the database name that we will return is inside our provided apps in route_app_labels
      if model._meta.app_label in self.route_app_labels:
         """return our database name -from settings.py file- that we are trying to setup this router for"""
         return 'users' 
      return None

   def db_for_write(self, model, **hints):
      """make attempts to provide the ability to write to our database"""
      if model._meta.app_label in self.route_app_labels:
         return 'users'
      return None

   def allow_relation(self, obj1, obj2, **hints):
      """allow relationships with our database if our app and database model is involved"""
      """here we are trying to ensure that only relationships can happens btn models inside my `user` app"""
      if (obj1._meta.app_label in self.route_app_labels
            or
          obj2._meta.app_label in self.route_app_labels):
            return True
      return None

   def allow_migrate(self, db, app_label, model_name=None, **hints):
      """make sure that user app is only appers in users database"""
      if app_label in self.route_app_labels:
         return db=='users'
      return None


#! The Commands to migrate:
# >> python manage.py migrate  --database=users
# >> python manage.py migrate --database=users
#! The Commands to create superuser:
# >> python manage.py createsuperuser --database=users
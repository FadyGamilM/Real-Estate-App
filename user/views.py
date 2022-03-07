from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializer
class RegisterView(APIView):
   # the project-level permission is => isAuthenticatedOnly, but to register you don't have to be authenticated
   permission_classes = (permissions.AllowAny,)
   def post(self, request):
      try:
         data = request.data
         name=data['name']
         email=data['email']
         # we need the email to be small letters to be able to check it agains all mails we have in DB
         email = email.lower()
         password=data['password']
         re_password=data['re_password']
         # the recieved data['is_relator'] is a string so we need to make it bool
         is_realtor=data['is_realtor']

         # decide if its realtor user or not
         if is_realtor == 'True':
            is_realtor = True
         else:
            is_realtor = False
         
         # check if password match the confirm_password
         if password==re_password:
            if len(password) >= 8:
               # filter this email agains all stored emails
               if not User.objects.filter(email=email).exists():
                  # check if this user is realtor or normal user
                  if is_realtor==True:
                     # create realtor user instance
                     User.objects.create_realtor(
                        name=name,
                        email=email,
                        password=password
                     )
                     # return the response
                     return Response({'success': 'Realtor is created successfully'}, status=status.HTTP_201_CREATED)
                  else:
                     # create normal user instance
                     User.objects.create_user(
                        name=name,
                        email=email,
                        password=password
                     )
                     # return the response
                     return Response({'success': 'user is created successfully'}, status=status.HTTP_201_CREATED)
               else:
                  return Response(
                     {'detail': 'This email is already exists'},
                     status=status.HTTP_400_BAD_REQUEST
                  )
            else:
               return Response(
                  {'detail': 'password must be at least 8 characters'},
                  status=status.HTTP_400_BAD_REQUEST
               )
         else:
            return Response(
               {'detail': 'passwords do not match'},
               status=status.HTTP_400_BAD_REQUEST
            )
      except:
         return Response(
            {'detail': 'Oops, something went wrong while registeration, please try again later'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )

class RetrieveUserView(APIView):
   """in order to access this view you have to be authenticated
      as the proejct-level permission is : isAuthenticated only, so
      you have to visit the api/token/ router in-order to get an access
      token to be authenticated .. """
   def get(self, request, format=None):
      try:
         # retrieve the user
         user = request.user
         # now we need to serialize these data from db 
         user = serializer.UserSerializer(user)
         # return the response with user data back to client
         return Response(
            {'user': user.data},
            status=status.HTTP_200_OK
         )
      except:
         return Response(
            {'detail': 'Oops, something went wrong while retrieveing user details'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )
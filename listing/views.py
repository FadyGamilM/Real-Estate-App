from rest_framework.views import APIView
from . import models
from rest_framework.response import Response 
from rest_framework import status
from .serializer import ListingSerializer
class ManageListingView(APIView):

   def get(self, request, format=None):
      """
         get all listing if slug is not passed as a query parameter -> all listings will be retrieved
         get specific listing detail if a query parameter is passed
      """
      try:
         # retrieve the user who make the request and check that this user is a realtor
         user = request.user
         if not user.is_realtor:
            return Response(
               {'detail': "Not Authorized"},
               # forbidden means authenticated but not authorized but 401 means that user is not even logged-in
               status=status.HTTP_403_FORBIDDEN
            )
         else:               
            # api/listing/manage?slug=gasgasgas
            slug = request.query_params.get('slug')
            if not slug:
               # retrieve back all listings
               listings = models.Listing.objects.order_by('-date_created').filter(realtor=user.email)
               # serialize the data from db based on the retrieved queryset
               listings = ListingSerializer(listings, many=True)
               return Response(
                  {'listings': listings.data},
                  status=status.HTTP_200_OK
               )
            else:
               if not models.Listing.objects.filter(realtor = user.email, slug=slug).exists():
                  return Response(
                     {'detail': 'listing is not found'},
                     status=status.HTTP_404_NOT_FOUND
                  )
               else:
                  listing = models.Listing.objects.get(realtor=user.email, slug=slug)
                  listing = ListingSerializer(listing)
                  return Response(
                     {'listing': listing.data},
                     status=status.HTTP_200_OK
                  )
      except:
         return Response(
            {'detail': 'Oops, something went wrong while retrieving listing\s, please try again later'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )
   
   def post(self, request):
      """
         only realtor user can use this view to create a new listing
         so we need authorization
      """
      try:
         #! step (1): retrieve the user who try to create this listing
         user = request.user
         #! step (2): make sure that this user is a realtor 
         if not user.is_realtor:
            return Response(
               {'detail': "Not Authorized"},
               # forbidden means authenticated but not authorized but 401 means that user is not even logged-in
               status=status.HTTP_403_FORBIDDEN
            )
         else:
            #! step (3): retrieve this json data
            data = request.data
            #! step (4): unpack the required fields from the dictionary data
            title = data['title']
            slug = data['slug']
            #! slug has to be unique so we have to check if we stored any listing with this slug before
            if models.Listing.objects.filter(slug=slug).exists():
               return Response(
                  {'detail': 'listing with this slug is already exists'},
                  status=status.HTTP_400_BAD_REQUEST,
               )
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            
            try:
               # if the string that passed through the price is not a number, for example the user typed "hello"
               price = int(data['price'])
            except:
               return Response(
                  {'detail': 'price must be an integer'},
                  status=status.HTTP_400_BAD_REQUEST,
               )

            try:
               bedrooms = int(data['bedrooms'])
            except:
               return Response(
                  {'detail': 'bedrooms must be a number'},
                  status=status.HTTP_400_BAD_REQUEST,
               )

            try:
               bathrooms = float(data['bathrooms'])
            except:
               return Response(
                  {'detail': 'bathrooms must be a floating point number'},
                  status=status.HTTP_400_BAD_REQUEST,
               )
            # lets also check that the bathrooms must be > 0 and <10 according to our model
            if bathrooms<=0 or bathrooms>=10:
               # set the default to be 1.0
               bathrooms=1.0
            # and finally round it to 1 decimal palce in case its not
            bathrooms = round(bathrooms, 1)
            
            sale_type = data['sale_type']
            if sale_type == 'FOR_SALE':
               sale_type = 'for sale'
            elif sale_type == 'FOR_RENT':
               sale_type = 'for rent'
            
            home_type = data['home_type']
            if home_type =='HOUSE':
               home_type = 'house'
            elif home_type=='CONDO':
               home_type = 'condo'
            elif home_type =='TOWNHOUSE':
               home_type = 'town house'
            
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']

            is_published = data['is_published']
            if is_published == 'True':
               is_published = True
            else:
               is_published = False
            

            #! step (5) : finally create the listing instance
            models.Listing.objects.create(
               realtor = user.email,
               title = title,
               slug = slug,
               address=address,
               city = city,
               state = state,
               zipcode = zipcode,
               description = description,
               price = price,
               bedrooms = bedrooms,
               bathrooms = bathrooms,
               main_photo = main_photo,
               photo_1 = photo_1,
               photo_2 = photo_2,
               photo_3 = photo_3,
               is_published=is_published,
            )
            #! step (6): return the response back
            return Response(
               {'success': 'listing is created successfully'},
               {'error': Response.errors},
               status=status.HTTP_201_CREATED,
            )
      except:
         return Response(
            {'detail': 'Oops, something went wrong while creating a new listing, please try again later'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
         )
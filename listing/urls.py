from django.urls import path
from . import views

urlpatterns = [
   path('manage/', views.ManageListingView.as_view()),
]
from .models import *
from .serializers import *

from django.http import JsonResponse
from rest_framework.generics import GenericAPIView


# Create your views here.


class ItemList(GenericAPIView):
    '''
    :param PK   An Integer
    :return  Item list of restaurant including item details
    '''

    def get_queryset(self):
        pk = self.kwargs.get('PK', None)

        if pk:
            return Restaurant.objects.filter(id=pk).first()

    def get(self, request, PK):
        restaurant = self.get_queryset()
        restaurant_serializer = RestaurantSerializer(restaurant)

        return JsonResponse(restaurant_serializer.data, safe=False)

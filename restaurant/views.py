import time

from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView


# Create your views here.
def response_200(data):
    """
    200
    :return:
    """
    response = {
        'Head': {
            'CallTime': int(round(time.time())),
            'Code': '200',
            'IsSuccess': True,
            'Message': 'Success',
        },
        'Result': data
    }
    return response


def response_404():
    """
    404
    :return:
    """
    response = {
        'Head': {
            'CallTime': int(round(time.time())),
            'Code': '404',
            'IsSuccess': False,
            'Message': 'Not Found',
        },
        'Result': []
    }

    return response


class ItemList(GenericAPIView):

    def get_queryset(self):
        # get restaurant query
        pk = self.kwargs.get('PK', None)

        if pk:
            return Restaurant.objects.filter(id=pk).first()

    def get(self, request, PK):
        '''

        :param request:
        :param PK: id of restaurant
        :return: Item list of restaurant including item details
        '''
        restaurant = self.get_queryset()

        # check the existence of restaurant data with different response
        if restaurant:
            restaurant_serializer = RestaurantSerializer(restaurant)
            response = response_200(restaurant_serializer.data)
        else:
            response = response_404()

        return JsonResponse(response, safe=False)

    def post(self, request):
        '''
        create restaurant with item, modifier, etc.
        '''
        data = request.data
        serializer = RestaurantSerializer(data=data)
        serializer.is_valid()
        restaurant = serializer.save()

        # output the created data for demonstration
        # restaurant_serializer = RestaurantSerializer(restaurant)
        # response = response_200(restaurant_serializer.data)

        return JsonResponse(response_200([]), safe=False)


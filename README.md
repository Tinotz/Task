
##Description:
    Utilizing your language of choice, design a RESTful web service API call that will return a list of menu items for a specific restaurant.
    For this API call, the front end will target path .

    ​/restaurant/:restaurantId/item​
    public Observable<Response> ​execute​(Request request) { ...
    URL url = ​new​ URL(​"https://api.presto.com/restaurant/1/item"​); HttpURLConnection con = url.openConnection();
    ...
    }
     The expected response will be parsed directly from JSON to a list of Item objects.
    ...
    execute(request).subscribe(response -> {
    Type listType = ​new​ TypeToken<List<Item>>(){}.getType();
    List<Item> items = ​new​ Gson().fromJson(response, listType); });
    ...
## Solution:
###### .views.py
```python


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
    '''
    :param PK   An Integer
    :return  Item list of restaurant including item details
    '''

    def get_queryset(self):
        # get restaurant query
        pk = self.kwargs.get('PK', None)

        if pk:
            return Restaurant.objects.filter(id=pk).first()

    def get(self, request, PK):
        restaurant = self.get_queryset()

        # check the existence of restaurant data with different response
        if restaurant:
            restaurant_serializer = RestaurantSerializer(restaurant)
            response = response_200(restaurant_serializer.data)
        else:
            response = response_404()

        return JsonResponse(response, safe=False)

    def post(self, request):
        data = request.data
        serializer = RestaurantSerializer(data=data)
        serializer.is_valid()
        restaurant = serializer.save()

        # output the created data for demonstration
        # restaurant_serializer = RestaurantSerializer(restaurant)
        # response = response_200(restaurant_serializer.data)

        return JsonResponse(response_200([]), safe=False)


```

###### .models.py
```python
from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.restaurant_name


class Item(models.Model):
    restaurant = models.ManyToManyField(Restaurant)
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name


class Modifier(models.Model):
    Item = models.ManyToManyField(Item)
    modifier_name = models.CharField(max_length=100)

    def __str__(self):
        return self.modifier_name


class SecondaryModifier(models.Model):
    modifier = models.ManyToManyField(Modifier)
    secondary_modifier_name = models.CharField(max_length=100)

    def __str__(self):
        return self.secondary_modifier_name
```

###### .serializers.py
```python
from .models import *
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers


class SecondaryModifierSerializer(serializers.ModelSerializer):
    '''secondary modifier serializer for serializing the its name'''

    secondary_modifier_name = serializers.CharField()

    class Meta:
        model = SecondaryModifier
        fields = ('secondary_modifier_name',)

    def create(self, validated_data):
        secondary_modifier = SecondaryModifier.objects.create(**validated_data)
        return secondary_modifier


class ModifierSerializer(serializers.ModelSerializer):
    '''modifier serializer for serializing the modifier name and its secondary modifiers'''

    modifier_name = serializers.CharField()
    # secondary_modifier = SecondaryModifierSerializer(many=True, read_only=True)

    secondary_modifier = serializers.SerializerMethodField()

    def get_secondary_modifier(self, obj):
        secondary_modifier = obj.secondarymodifier_set.all()

        if secondary_modifier is not None and len(secondary_modifier) > 0:
            return SecondaryModifierSerializer(secondary_modifier, many=True).data
        else:
            return ""

    class Meta:
        model = Modifier
        fields = ('modifier_name', 'secondary_modifier')

    def create(self, validated_data):
        secondary_modifier_data = self.initial_data.pop('secondary_modifier')
        modifier = Modifier.objects.create(**validated_data)

        for secondary_modifier in secondary_modifier_data:
            serializer = SecondaryModifierSerializer(data=secondary_modifier)
            serializer.is_valid()
            obj = serializer.save()
            modifier.secondarymodifier_set.add(obj)
        return modifier


class ItemSerializer(serializers.ModelSerializer):
    '''item serializer for serializing the item name and its modifiers'''

    item_name = serializers.CharField()
    # modifier = ModifierSerializer(many=True, read_only=True)

    modifier = serializers.SerializerMethodField()

    def get_modifier(self, obj):
        modifier = obj.modifier_set.all()

        if modifier is not None and len(modifier) > 0:
            return ModifierSerializer(modifier, many=True).data
        else:
            return ""

    class Meta:
        model = Item
        fields = ('item_name', 'modifier')

    def create(self, validated_data):
        modifier_data = self.initial_data.pop('modifier')
        item = Item.objects.create(**validated_data)

        for modifier in modifier_data:
            serializer = ModifierSerializer(data=modifier)
            serializer.is_valid()
            obj = serializer.save()
            item.modifier_set.add(obj)
        return item


class RestaurantSerializer(serializers.ModelSerializer):
    '''restaurant serializer for serializing the name and item set'''

    restaurant_name = serializers.CharField()
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'restaurant_name', 'item_set')

    def create(self, validated_data):
        item_data = self.initial_data.pop('item_set')
        restaurant = Restaurant.objects.create(**validated_data)

        for item in item_data:
            serializer = ItemSerializer(data=item)
            serializer.is_valid()
            obj = serializer.save()
            restaurant.item_set.add(obj)

        # another way to create the nested data

        # for item in item_data:
        #     item_obj, created = Item.objects.get_or_create(item_name=item['item_name'])
        #     restaurant.item_set.add(item_obj)
        #     modifier_data = item.pop('modifier')
        #     for modifier in modifier_data:
        #         modifier_obj, created = Modifier.objects.get_or_create(modifier_name=modifier['modifier_name'])
        #         item_obj.modifier_set.add(modifier_obj)
        #         secondary_modifier_data = modifier.pop('secondary_modifier')
        #         for secondary_modifier in secondary_modifier_data:
        #             secondary_modifier_obj, created = SecondaryModifier.objects.get_or_create(
        #                 secondary_modifier_name=secondary_modifier['secondary_modifier_name'])

        return restaurant

```

    Initiated 8.31.2018

    1. Used Django-Restful-Framework with MYSQL.
    2. Created Restaurant, Item, Modifier, and SecondaryModifier models. Restaurant and Item models can be manytomany
    because there could be one restaurant have many items and one same item can appear in different restaurant. This
    can somehow reduce the repeatable data.
    3. Used GET request to communicate with front-end. If there is more time, it can also have full sets of RESTful APIs.
    However I managed to put Django admin to adding or updating the data through Django admin site.
    4. Scalability wise, we can add extra fields for restaurant, item and etc easily. The api has been tested by the
    Jmeter with 100 users at same time and 10 loops for local environment requests.

    updated 9.9.2018
    1. now the api is able to create a new restaurant with items, modifiers, etc in json form. url: /create/item


## Requirements:
    Django==1.11
    djangorestframework==3.7.7
    drf-writable-nested==0.5.0



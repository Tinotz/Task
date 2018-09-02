
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


from .models import *
from .serializers import *

from django.http import JsonResponse
from rest_framework.generics import GenericAPIView


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
```

###### .models.py
```python
from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)


class Item(models.Model):
    restaurant = models.ManyToManyField(Restaurant)
    item_name = models.CharField(max_length=100, unique=True)


class Modifier(models.Model):
    Item = models.ManyToManyField(Item)
    modifier_name = models.CharField(max_length=100, unique=True)


class SecondaryModifier(models.Model):
    modifier = models.ManyToManyField(Modifier)
    secondary_modifier_name = models.CharField(max_length=100, unique=True)
```
###### .serializers.py
```python
from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class SecondaryModifierSerializer(serializers.ModelSerializer):
    secondary_modifier_name = serializers.CharField()

    class Meta:
        model = SecondaryModifier
        fields = ('secondary_modifier_name',)


class ModifierSerializer(WritableNestedModelSerializer):
    modifier_name = serializers.CharField()
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


class ItemSerializer(WritableNestedModelSerializer):
    item_name = serializers.CharField()
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


class RestaurantSerializer(WritableNestedModelSerializer):
    restaurant_name = serializers.CharField()
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('restaurant_name', 'item_set')
```

    Initiated 8.31.2018

    1. Used Django-Restful-Framework with MYSQL.
    2. Created Restaurant, Item, Modifier, and SecondaryModifier models.
    3. Used GET request to communicate with front-end. If there is more time, it can be built with Restful APIs.


## Requirements:
    Django==1.11
    djangorestframework==3.7.7
    drf-writable-nested==0.5.0



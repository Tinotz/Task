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

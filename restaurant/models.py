from django.db import models


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.restaurant_name


class Item(models.Model):
    restaurant = models.ManyToManyField(Restaurant)
    item_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.item_name


class Modifier(models.Model):
    Item = models.ManyToManyField(Item)
    modifier_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.modifier_name


class SecondaryModifier(models.Model):
    modifier = models.ManyToManyField(Modifier)
    secondary_modifier_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.secondary_modifier_name

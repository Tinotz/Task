from django.contrib import admin
from .models import *


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant_name')

    class Meta:
        model = Restaurant
        fields = '__all__'

    def __str__(self):
        return Restaurant.restaurant_name


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name')

    class Meta:
        model = Item
        fields = '__all__'

    def __str__(self):
        return Item.item_name


@admin.register(Modifier)
class ModifierAdmin(admin.ModelAdmin):
    list_display = ('id', 'modifier_name')

    class Meta:
        model = Modifier
        fields = '__all__'

    def __str__(self):
        return Modifier.modifier_name


@admin.register(SecondaryModifier)
class SecondaryModifierAdmin(admin.ModelAdmin):
    list_display = ('id', 'secondary_modifier_name')

    class Meta:
        model = SecondaryModifier
        fields = '__all__'

    def __str__(self):
        return SecondaryModifier.secondary_modifier_name

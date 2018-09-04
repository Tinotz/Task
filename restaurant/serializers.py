from .models import *
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers


class SecondaryModifierSerializer(serializers.ModelSerializer):
    '''secondary modifier serializer for serializing the its name'''

    secondary_modifier_name = serializers.CharField()

    class Meta:
        model = SecondaryModifier
        fields = ('secondary_modifier_name',)


class ModifierSerializer(WritableNestedModelSerializer):
    '''modifier serializer for serializing the modifier name and its secondary modifiers'''

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
    '''item serializer for serializing the item name and its modifiers'''

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
    '''restaurant serializer for serializing the name and item set'''

    restaurant_name = serializers.CharField()
    item_set = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('restaurant_name', 'item_set')

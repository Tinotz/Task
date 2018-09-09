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

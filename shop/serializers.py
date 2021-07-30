from rest_framework import serializers

from .models import City, Street, Shop


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('title',)


class StreetSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(write_only=True)
    city = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Street
        fields = ('title', 'city',)


class ShopSerializer(serializers.ModelSerializer):
    city_id = serializers.IntegerField(write_only=True)
    city = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    street_id = serializers.IntegerField(write_only=True)
    street = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Shop
        fields = ('title', 'city', 'city_id', 'street', 'street_id', 'home',
                  'opening_time', 'closing_time')

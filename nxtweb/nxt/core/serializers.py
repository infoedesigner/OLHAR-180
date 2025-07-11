from rest_framework import serializers

from nxt.core.models import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'state',
        ]

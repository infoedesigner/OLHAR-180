from rest_framework import serializers

from nxt.clients.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'client',
            'parent',
        ]

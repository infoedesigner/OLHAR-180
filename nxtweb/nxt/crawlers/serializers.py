from rest_framework import serializers

from nxt.crawlers.models import Execution


class ExecutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Execution
        fields = [
            'id',
            'crawler',
            'finish',
            'status',
            'error_details',
            'log',
            'created',
            'modified',
        ]
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from nxt.core.serializers import CitySerializer
from nxt.core.models import City


class CityViewSet(viewsets.ReadOnlyModelViewSet):

    pagination_class = None
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    queryset = City.objects.filter(is_active=True)
    filterset_fields = ['state']

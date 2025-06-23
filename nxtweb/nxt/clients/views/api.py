from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from nxt.clients.models import Category
from nxt.clients.serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['client']

    def get_queryset(self):
        return Category.objects.filter(client__company=self.request.user.company)

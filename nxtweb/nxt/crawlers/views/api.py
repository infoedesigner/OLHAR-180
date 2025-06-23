from rest_framework import viewsets

from nxt.security.permissions import IsSupeuser

from nxt.crawlers.models import Execution
from nxt.crawlers.serializers import ExecutionSerializer


class ExecutionViewSet(viewsets.ModelViewSet):

    serializer_class = ExecutionSerializer
    queryset = Execution.objects.all()
    permission_classes = [IsSupeuser]

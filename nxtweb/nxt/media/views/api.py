from rest_framework import viewsets

from nxt.security.permissions import IsSupeuser, IsNXTAdmin

from nxt.media.serializers import (
    SourceSerializer, MediaSerializer, MediaContentSerializer, EditorialSerializer
)
from nxt.media.models import Source, Media, MediaContent, Editorial
from nxt.media.filters import (
    SourceFilterSet, MediaFilterSet, MediaContentFilterSet, EditorialFilterSet
)


class SourceViewSet(viewsets.ModelViewSet):

    permission_classes = [IsSupeuser]
    queryset = Source.objects.all()
    filterset_class = SourceFilterSet
    serializer_class = SourceSerializer


class MediaViewSet(viewsets.ModelViewSet):

    permission_classes = [IsSupeuser]
    queryset = Media.objects.all()
    filterset_class = MediaFilterSet
    serializer_class = MediaSerializer


class MediaContentViewSet(viewsets.ModelViewSet):

    permission_classes = [IsSupeuser]
    queryset = MediaContent.objects.all()
    filterset_class = MediaContentFilterSet
    serializer_class = MediaContentSerializer


class EditorialViewSet(viewsets.ModelViewSet):

    permission_classes = [IsNXTAdmin]
    serializer_class = EditorialSerializer
    filterset_class = EditorialFilterSet
    fieldset_fields = ['source']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Editorial.objects.all()
        return Editorial.objects.filter(source__company=self.request.user.company)

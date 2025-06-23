from django_filters.filterset import FilterSet

from nxt.media.models import Source, Media, MediaContent, Editorial


class SourceFilterSet(FilterSet):

    class Meta:
        model = Source
        fields = {
            'company': ['exact'],
            'source_type': ['exact'],
            'is_active': ['exact'],
        }


class MediaFilterSet(FilterSet):

    class Meta:
        model = Media
        fields = {
            'source': ['exact'],
            'media_content_type': ['exact', 'in']
        }


class MediaContentFilterSet(FilterSet):

    class Meta:
        model = MediaContent
        fields = {
            'media': ['exact'],
        }


class EditorialFilterSet(FilterSet):

    class Meta:
        model = Editorial
        fields = {
            'source': ['exact'],
        }

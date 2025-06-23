from django.utils.html import strip_tags

from rest_framework import serializers

from nxt.media.models import Media, Source, MediaContent, Editorial


class EditorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Editorial
        fields = [
            'id',
            'source',
            'name',
            'url',
            'url_xpath',
            'date_xpath',
            'date_format',
            'title_xpath',
            'author_xpath',
            'text_xpath',
            'use_configuration_source',
            'created',
            'modified',
        ]

class SourceSerializer(serializers.ModelSerializer):

    editorials = EditorialSerializer(many=True)

    class Meta:
        model = Source
        fields = [
            'id',
            'name',
            'source_type',
            'territory_id',
            'priority',
            'marketing_value',
            'company',
            'city',
            'state',
            'website',
            'frequency',
            'publish_days',
            'is_active',
            'editorials',
            'url_root',
            'url_xpath',
            'date_xpath',
            'date_format',
            'title_xpath',
            'author_xpath',
            'text_xpath',
            'created',
            'modified',
        ]


class MediaSerializer(serializers.ModelSerializer):

    def validate_title(self, value):
        return strip_tags(value)

    def validate_authors(self, value):
        return strip_tags(value)

    def validate_resume(self, value):
        return strip_tags(value)

    def validate_publish_date_raw(self, value):
        return strip_tags(value)

    def validate(self, attrs):
        source = attrs.get('source')
        url = attrs.get('url')
        if source and url:
            if source.medias.filter(url=url).exists():
                raise serializers.ValidationError({'url': 'Notícia já existente com esta url'})
        return attrs


    class Meta:
        model = Media
        fields = [
            'id',
            'title',
            'media_content_type',
            'url',
            'source',
            'editorial',
            'publish_date',
            'publish_date_raw',
            'resume',
            'authors',
            'image',
            'is_active',
            'created',
            'modified',
        ]


class MediaContentSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        transcription = attrs.get('transcription')
        media = attrs.get('media')
        if media and transcription and media.source.source_type == 'site':
            pass
        return attrs

    class Meta:
        model = MediaContent
        fields = [
            'id',
            'media',
            'order',
            'document',
            'transcription',
            'processed',
            'errors',
            'is_active',
            'created',
            'modified',
        ]

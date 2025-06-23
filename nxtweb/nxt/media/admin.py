from django.contrib import admin

from nxt.media.models import Source, Editorial, Media, MediaContent, Newspaper


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):

    list_display = ['source', 'publish_date', 'is_active', 'created', 'modified']
    search_fields = ['source__name']
    list_filter = ['publish_date']


@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):

    list_display = ['media', 'order', 'is_active', 'created', 'modified']
    search_fields = ['media__title', 'transcription']


class MediaContentInline(admin.StackedInline):

    extra = 0
    model = MediaContent


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):

    list_display = ['title', 'source', 'publish_date', 'created']
    search_fields = ['title', 'source__name']
    inlines = [MediaContentInline]
    list_filter = ['source__source_type']


class EditorialInline(admin.StackedInline):

    model = Editorial
    extra = 1


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    list_display = ['name', 'source_type', 'company']
    search_fields = ['name']
    list_filter = ['company']
    inlines = [EditorialInline]

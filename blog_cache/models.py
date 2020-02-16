from markdown_blog import settings
from django.db import models
from os import path


# Hack for creating dynamic migrations
class StringSettingsReference(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return getattr(settings, self.name)

    def deconstruct(self):
        return "%s.%s" % (__name__, self.__class__.__name__), (self.name,), {}


# Image cache model
class ImageCache(models.Model):
    file = models.FilePathField(path=StringSettingsReference('UPLOAD_FOLDER'), recursive=True, unique=True)
    fileType = models.CharField(max_length=24)
    altText = models.CharField(max_length=120, blank=True, null=True)
    cachedSmall = models.FilePathField(path=StringSettingsReference('STATIC_FOLDER'), recursive=True)
    cachedMedium = models.FilePathField(path=StringSettingsReference('STATIC_FOLDER'), recursive=True)
    cachedLarge = models.FilePathField(path=StringSettingsReference('STATIC_FOLDER'), recursive=True)
    fileHash = models.CharField(max_length=160)
    lastCached = models.DateTimeField()
    isPortrait = models.BooleanField()
    exifData = models.TextField(blank=True, null=True)

    GENERIC_TYPE = 'generic'
    CATEGORY_TYPE = 'category'
    PAGE_TYPE = 'page'

    SMALL = 200, 200
    MEDIUM = 1000, 1000
    LARGE = 2000, 2000

    def __str__(self):
        return self.altText

    def url_small(self):
        return path.join(settings.STATIC_IMAGE_CACHE_URL, path.basename(self.cachedSmall))

    def url_medium(self):
        return path.join(settings.STATIC_IMAGE_CACHE_URL, path.basename(self.cachedMedium))

    def url_large(self):
        return path.join(settings.STATIC_IMAGE_CACHE_URL, path.basename(self.cachedLarge))

    def portrait_class(self):
        if self.isPortrait:
            return 'portrait'
        return ''


# Category cache model
class CategoryCache(models.Model):
    folder = models.FilePathField(path=StringSettingsReference('UPLOAD_FOLDER'), allow_files=False, allow_folders=True, unique=True)
    file = models.FilePathField(path=StringSettingsReference('UPLOAD_FOLDER'), recursive=True)
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    featureImage = models.ForeignKey('ImageCache', on_delete=models.DO_NOTHING, blank=True, null=True)
    fileHash = models.CharField(max_length=160)
    lastCached = models.DateTimeField()

    def __str__(self):
        return self.title

    # TODO: Make dynamic subdir setting
    def url(self):
        return '/' + self.slug


# Tag cache model
class TagCache(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.title

    # TODO: Make dynamic subdir setting
    def url(self):
        return '/tag/' + self.slug


# Article cache model
class ArticleCache(models.Model):
    file = models.FilePathField(path=StringSettingsReference('UPLOAD_FOLDER'), recursive=True, unique=True)
    fileHash = models.CharField(max_length=160)
    slug = models.SlugField(max_length=240)
    title = models.CharField(max_length=240)
    description = models.TextField(blank=True, null=True)
    published = models.DateTimeField()
    author = models.CharField(max_length=120, blank=True, null=True)
    cachedHeading = models.CharField(max_length=240)
    cachedContent = models.TextField()
    draft = models.BooleanField()
    lastCached = models.DateTimeField()
    category = models.ForeignKey(CategoryCache, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(TagCache)
    featureImage = models.ForeignKey('ImageCache', on_delete=models.DO_NOTHING, blank=True, null=True)
    extraData = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    # TODO: Make dynamic subdir setting
    def url(self):
        return '/' + self.category.slug + '/' + self.slug

    class Meta:
        unique_together = ('slug', 'category')

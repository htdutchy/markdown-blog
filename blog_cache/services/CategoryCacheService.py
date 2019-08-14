import logging
from ..models import CategoryCache, ImageCache
from ..services import ImageCacheService
from pytz import timezone
from os import path
from glob import glob
from markdown_blog import settings
from ..helpers.MarkdownHelper import Markdown
from ..helpers import HashHelper
from datetime import datetime

logger = logging.getLogger('blog.caching.category')


def add(folder):
    logger.info('Adding category: ' + folder)
    file = path.join(folder, '_meta.md')
    file_hash = HashHelper.sha256_file(file)
    md = Markdown(file)

    category = CategoryCache(
        folder=folder,
        file=file,
        fileHash=file_hash,
        slug=md.slug,
        title=md.title,
        description=md.description,
        lastCached=datetime.now(tz=timezone(settings.TIME_ZONE))
    )

    if md.featureImage:
        feature_image_file = path.join(category.folder, md.featureImage)
        if path.isfile(feature_image_file):
            feature_image = ImageCacheService.magic_image(feature_image_file, ImageCache.CATEGORY_TYPE, md.featureImage)
            if feature_image:
                category.featureImage = feature_image

    try:
        category.save()
    except Exception as e:
        logger.error('Failed to add category: ' + folder)
        logger.error('Original message:' + str(e))


def update(category, file_hash):
    logger.info('Updating category: ' + category.folder)
    md = Markdown(category.file)
    category.fileHash = file_hash
    category.slug = md.slug
    category.title = md.title
    category.description = md.description
    category.lastCached=datetime.now(tz=timezone(settings.TIME_ZONE))

    if md.featureImage:
        feature_image_file = path.join(category.folder, md.featureImage)
        if path.isfile(feature_image_file):
            feature_image = ImageCacheService.magic_image(feature_image_file, ImageCache.CATEGORY_TYPE, md.featureImage)
            if feature_image:
                category.featureImage = feature_image

    try:
        category.save()
    except Exception as e:
        logger.error('Failed to update category: ' + category.folder)
        logger.error('Original message:' + str(e))


def delete(category):
    logger.info('Deleting category: ' + category.folder)
    category.delete()


def check_new():
    folders = glob(settings.UPLOAD_FOLDER+'/*/')
    for folder in folders:
        logger.debug('Found category: ' + folder)
        if path.isfile(path.join(folder, '_meta.md')):
            try:
                category = CategoryCache.objects.get(folder__exact=folder)
            except CategoryCache.DoesNotExist:
                category = False
            if not category:
                add(folder)


def check_existing():
    for category in CategoryCache.objects.all():
        logger.debug('Checking category: ' + category.folder)
        if not path.isdir(category.folder):
            delete(category)
            continue
        file_hash = HashHelper.sha256_file(category.file)
        if file_hash != category.fileHash:
            update(category, file_hash)


import logging
from ..helpers import HashHelper
from ..models import ImageCache
from markdown_blog import settings
from os import path, mkdir, remove
from PIL import Image
from pytz import timezone
from datetime import datetime
import uuid

logger = logging.getLogger('blog.caching.image')


def generate_image(file, size):
    logger.info('Generating image: ' + file + ' at size:' + str(size))
    try:
        if not path.isdir(settings.STATIC_IMAGE_CACHE_FOLDER):
            mkdir(settings.STATIC_IMAGE_CACHE_FOLDER)
        im = Image.open(file)
        new_file = path.join(settings.STATIC_IMAGE_CACHE_FOLDER, str(uuid.uuid4()) + '.jpeg')
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(new_file, "JPEG")
        logger.info('Saved image: ' + new_file)
        return new_file
    except IOError as e:
        logger.error('Could not save image: ' + file)
        logger.error('Original message: ' + str(e))
    return None


def magic_image(file, type, alt):
    logger.debug('Magic image request:' + file + ' type: ' + type + ' alt: ' + alt)
    if not path.isfile(file):
        return None
    try:
        image = ImageCache.objects.get(file__exact=file, fileType__exact=type)
    except ImageCache.DoesNotExist:
        image = None
    if not image:
        image = ImageCache(
            file=file,
            fileType=type
        )
    image.altText = alt
    image.lastCached = datetime.now(tz=timezone(settings.TIME_ZONE))
    file_hash = HashHelper.sha256_file(file)
    refresh = False
    if file_hash != image.fileHash:
        refresh = True
        image.fileHash = file_hash
    if refresh or not path.isfile(image.cachedSmall):
        if path.isfile(image.cachedSmall):
            remove(image.cachedSmall)
        image.cachedSmall = generate_image(file, ImageCache.SMALL)
    if refresh or not path.isfile(image.cachedMedium):
        if path.isfile(image.cachedMedium):
            remove(image.cachedMedium)
        image.cachedMedium = generate_image(file, ImageCache.MEDIUM)
    if refresh or not path.isfile(image.cachedLarge):
        if path.isfile(image.cachedLarge):
            remove(image.cachedLarge)
        image.cachedLarge = generate_image(file, ImageCache.LARGE)

    try:
        image.save()
    except Exception as e:
        logger.error('Failed to save image: ' + file)
        logger.error('Original message: ' + str(e))
        return None
    return image


def check_existing():
    for image in ImageCache.objects.all():
        magic_image(image.file, image.fileType, image.altText)

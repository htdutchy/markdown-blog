import logging
from ..models import ArticleCache, CategoryCache, ImageCache
from pytz import timezone
from os import path
from glob import glob
from ..services import TagCacheService, ImageCacheService
from markdown_blog import settings
from ..helpers.MarkdownHelper import Markdown
from ..helpers import HashHelper
from datetime import datetime

logger = logging.getLogger('blog.caching.page')


def add(file, category):
    logger.info('Adding page: ' + file)
    file_hash = HashHelper.sha256_file(file)
    md = Markdown(file)

    page = ArticleCache(
        file=file,
        fileHash=file_hash,
        slug=md.slug,
        title=md.title,
        description=md.description,
        published=datetime.now(tz=timezone(settings.TIME_ZONE)),
        author=md.author,
        cachedHeading = md.soup.h1.extract().string,
        cachedContent = str(md.soup),
        draft=md.isDraft,
        lastCached=datetime.now(tz=timezone(settings.TIME_ZONE)),
        category=category,
    )

    if md.featureImage:
        feature_image_file = path.join(category.folder, md.featureImage)
        if path.isfile(feature_image_file):
            feature_image = ImageCacheService.magic_image(feature_image_file, ImageCache.PAGE_TYPE, md.featureImage)
            if feature_image:
                page.featureImage = feature_image

    try:
        page.save()
        for tag_title in md.tags:
            tag = TagCacheService.magic_tag(tag_title)
            if tag:
                page.tags.add(tag)
        page.save()
    except Exception as e:
        logger.error('Failed to add page: ' + file)
        logger.error('Original message:' + str(e))


def update(page, file_hash):
    logger.info('Updating page: ' + page.file)
    md = Markdown(page.file)

    page.fileHash = file_hash
    page.slug = md.slug
    page.title = md.title
    page.description = md.description
    page.author = md.author
    page.cachedHeading = md.soup.h1.extract().string
    page.cachedContent = str(md.soup)
    page.draft = md.isDraft
    page.lastCached=datetime.now(tz=timezone(settings.TIME_ZONE))

    if md.featureImage:
        feature_image_file = path.join(page.category.folder, md.featureImage)
        if path.isfile(feature_image_file):
            feature_image = ImageCacheService.magic_image(feature_image_file, ImageCache.PAGE_TYPE, md.featureImage)
            if feature_image:
                page.featureImage = feature_image

    try:
        page.save()
        for tag in page.tags.all():
            page.tags.remove(tag)
        for tag_title in md.tags:
            tag = TagCacheService.magic_tag(tag_title)
            if tag:
                page.tags.add(tag)
        page.save()
    except Exception as e:
        logger.error('Failed to update page: ' + page.file)
        logger.error('Original message:' + str(e))


def delete(page):
    logger.info('Deleting page: ' + page.file)
    page.delete()


def check_new():
    for category in CategoryCache.objects.all():
        files = glob(category.folder+'/[!_]*.md')
        for file in files:
            logger.debug('Found page: ' + file)
            if path.isfile(file):
                try:
                    page = ArticleCache.objects.get(file__exact=file)
                except ArticleCache.DoesNotExist:
                    page = False
                if not page:
                    add(file, category)


def check_existing():
    for page in ArticleCache.objects.all():
        logger.debug('Checking page: ' + page.file)
        if not path.isfile(page.file):
            delete(page)
            continue
        file_hash = HashHelper.sha256_file(page.file)
        if file_hash != page.fileHash:
            update(page, file_hash)

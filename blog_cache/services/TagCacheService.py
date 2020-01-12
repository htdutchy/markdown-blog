import logging
from slugify import slugify
from ..models import TagCache, ArticleCache

logger = logging.getLogger('blog.caching.tag')


def magic_tag(title):
    title_slug = slugify(title)
    logger.debug('Magic tag request: ' + title_slug)
    try:
        tag = TagCache.objects.get(slug__iexact=title_slug)
        return tag
    except TagCache.DoesNotExist:
        pass
    logger.info('Adding tag:' + title_slug)
    tag = TagCache(title=title, slug=title_slug)
    try:
        tag.save()
    except Exception as e:
        logger.error('Failed to save tag: ' + title_slug)
        logger.error('Original message:' + str(e))
    return tag


def kill_orphans():
    logger.info('Killing orphaned tags')
    try:
        orphans = TagCache.objects.exclude(pk__in=ArticleCache.tags.through.objects.values('tagcache'))
        orphans.delete()
    except Exception as e:
        logger.error('Failed to delete orphaned tags')
        logger.error('Original message:' + str(e))

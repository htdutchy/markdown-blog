import logging
from ..models import TagCache, ArticleCache

logger = logging.getLogger('blog.caching.tag')


def magic_tag(title):
    logger.debug('Magic tag request: ' + title)
    try:
        tag = TagCache.objects.get(title__iexact=title)
        return tag
    except TagCache.DoesNotExist:
        pass
    logger.info('Adding tag:' + title)
    tag = TagCache(title=title)
    try:
        tag.save()
    except Exception as e:
        logger.error('Failed to save tag: ' + title)
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

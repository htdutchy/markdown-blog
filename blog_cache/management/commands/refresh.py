from django.core.management.base import BaseCommand, CommandError
from ...services import ArticleCacheService, CategoryCacheService, TagCacheService, ImageCacheService


class Command(BaseCommand):
    help = 'Refresh blog cache'

    def handle(self, *args, **options):
        CategoryCacheService.check_existing()
        CategoryCacheService.check_new()
        ArticleCacheService.check_existing()
        ArticleCacheService.check_new()
        TagCacheService.kill_orphans()
        ImageCacheService.check_existing()

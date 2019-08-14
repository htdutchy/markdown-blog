from django.core.management.base import BaseCommand, CommandError
from ...services import ArticleCacheService, CategoryCacheService


class Command(BaseCommand):
    help = 'Reload blog cache'

    def handle(self, *args, **options):
        print("Not yet implemented")


from markdown_blog import settings
from django.shortcuts import render
from blog_cache.models import CategoryCache, ArticleCache


# Create your views here.
def index_action(request):
    categories = CategoryCache.objects.all()
    articles = ArticleCache.objects.filter(draft=False).order_by('published').all()[:5]

    context = {
        'meta_title': 'Home',
        'header_title': 'Home',
        'html': '',
        'categories': categories,
        'articles': articles,
    }
    return render(request, 'index.html', context)


def category_action(request, category_slug):
    return render(request, 'base.html')


def article_action(request, category_slug, page_slug):
    return render(request, 'base.html')

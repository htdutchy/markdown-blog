from markdown_blog import settings
from django.shortcuts import render
from blog_cache.models import CategoryCache, ArticleCache


# Create your views here.
def index_action(request):
    categories = CategoryCache.objects.order_by('title').all()
    articles = ArticleCache.objects.filter(draft=False).order_by('published').all()[:5]

    context = {
        'background_img': 'default.jpg',
        'meta_title': 'Categories',
        'header_title': 'Categories',
        'html': '',
        'categories': categories,
        'articles': articles,
    }
    return render(request, 'categories.html', context)


def category_action(request, category_slug):
    category = CategoryCache.objects.get(slug__exact=category_slug)
    if not category:
        return render(request, '404.html')

    articles = category.articlecache_set.filter(draft=False).order_by('published').all()

    context = {
        'background_img': category.featureImage.url_large,
        'meta_title': 'Category: ' + category.title,
        'header_title': 'Category: ' + category.title,
        'html': '',
        'category': category,
        'articles': articles,
    }
    return render(request, 'category.html', context)


def article_action(request, category_slug, article_slug):
    article = ArticleCache.objects.get(category__slug=category_slug, slug=article_slug, draft=False)

    articles = article.category.articlecache_set.filter(draft=False).order_by('published').all()[:5]

    context = {
        'background_img': article.featureImage.url_large,
        'meta_title': article.title,
        'header_title': article.cachedHeading,
        'html': article.cachedContent,
        'article': article,
        'articles': articles,
    }
    return render(request, 'article.html', context)

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_action, name='index'),
    path('<str:category_slug>', views.category_action, name='category'),
    path('<str:category_slug>/<str:page_slug>', views.article_action, name='article'),
]

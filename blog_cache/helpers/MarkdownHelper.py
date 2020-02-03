import markdown, codecs
from markdown_blog import settings
from bs4 import BeautifulSoup


class Markdown:
    def __init__(self, filepath):
        text = codecs.open(filepath, mode="r").read()
        md = markdown.Markdown(extensions=settings.MARKDOWN_EXTENSIONS)
        self.html = md.convert(text)
        self.soup = BeautifulSoup(self.html, 'html.parser')
        meta = md.Meta

        try:
            self.title = str(meta['title'][0])
        except KeyError:
            self.title = None

        try:
            self.slug = str(meta['slug'][0])
        except KeyError:
            self.slug = None

        try:
            self.description = str(meta['description'][0])
        except KeyError:
            self.description = None

        try:
            self.tags = list(map(str.strip, str(meta['tags'][0]).split(',')))
        except KeyError:
            self.tags = []

        try:
            self.featureImage = str(meta['feature_image'][0])
        except KeyError:
            self.featureImage = None

        try:
            self.author = str(meta['author'][0])
        except KeyError:
            self.author = None

        self.isDraft = False
        try:
            self.isDraft = str(meta['draft'][0]).lower() in ("yes", "true", "t", "1")
        except KeyError:
            pass

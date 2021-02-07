# Markdown Blog

## A blogging engine written in Django, no wysiwyg, just upload .md files!

**This is a work in progress, readme isn't complete yet but poc is almost finished**

While there are applications that convert your markdown files into a website, they don't do a very good job of making a modern website.  
This project aims to generate modern, advanced websites from basic folder structures and markdown files.
Besides taking a basic folder structure with markdown files there is support for meta data to add SEO and select featured images.  

More advanced features will include:
- MermaidJS support
- CodeHilite
- Image EXIF data parsing
- Image galleries

If you want to use this system for yourself you can either use the included frontend app or override it with your own.
I'm working on an official way to smoothly integrate custom frontends that won't be broken by a code base update.

### Installation
```bash
# Create virtual environment
python3 -m venv venv
# Open virtual environment
source venv/bin/activate
# Install python requirements
pip install -r requirements.txt
# Copy .env file and edit to desired settings
cp .env.example .env
nano .env
# Initiate the database
./manage.py migrate
```

### Usage:
#### Category creation:
Create a folder in your upload directory.  
To keep things simple I advise using the slug as folder name (`upload/example_category`).

Create the metadata file (`upload/example_categoy/_meta.md`).

    slug: example_category
    title: Example category
    description: Just an example
    feature_image: _category.jpg

Upload the feature_image (`upload/example_category/_category.jpg`)

#### Blog post creation:

Upload the markdown file:

    author: your name here
    slug: article_1
    title: The first article
    description: Some article has to go first, might as well be this one!
    tags: first, tag, you're, it!
    feature_image: some_image.jpg
    draft: true
    
    # This is a title
    
    ## The amazing subtitle to the title
    
    ### First paragraph
    
    This is a block of text.  
    Line spacing
    
    - un
    - ordered
    - list
    
    1. ordered
    2. list
    
    head1 | head2
    :---: | :---
    item 1 | item2
    
    **bold text**
    
    - [ ] unchecked
    - [x] checked

Upload the feature_image (`upload/example_category/some_image.jpg`)

### Development
```bash
# Install npm requirements (only required for development)
npm install
# Run the django dev server
./manage.py runserver
# Run gulp watcher & browserSync
gulp browserSync
```

### Deployment
#### Standard (cron + systemd)

#### Docker

### Credits

frontend default.jpg: [shopify burst]('https://burst.shopify.com/photos/camping-kettle-and-coffee-cup?c=nature')

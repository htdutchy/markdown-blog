# Markdown Blog

## A blogging engine written in Django, no wysiwyg, just upload .md files!

While there are applications that convert your markdown files into a website, they don't do a very good job.  
This is the solution.

This system will do a lot of fancy work like caching, image optimization  
and every possible thing I can think of to bring a markdown based blog up to modern standards and maybe to the cutting edge of technology.  
(I will be ignoring IE11 during development of my blog, if you want backwards compatability, it's up to you)

## Documentation will follow, this project is still in development

If you want to use this system for yourself, feel free to fork this project!

## Usage:
### Category creation:
Create a folder in your upload directory.  
To keep things simple I advise using the slug as folder name (`upload/example_category`).

Create the metadata file (`upload/example_categoy/_meta.md`.

    slug: example_category
    title: Example category
    description: Just an example
    feature_image: _category.jpg

Upload the feature_image (`upload/example_category/_category.jpg`)

### Blog post creation:

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

### Credits

frontend default.jpg: [shopify burst]('https://burst.shopify.com/photos/camping-kettle-and-coffee-cup?c=nature')

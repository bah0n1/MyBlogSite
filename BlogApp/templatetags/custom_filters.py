# templatetags/custom_filters.py
from django import template
from BlogApp.models import Tag,Post,Categories,Author

register = template.Library()

@register.filter
def first_tag(tags):
    return tags.first() if tags.exists() else None
@register.filter
def contentOntag(categorie):
    count = Post.objects.filter(categories=categorie).count()
    return count

@register.filter
def AuthorPost(author):
    count = Post.objects.filter(author__name=author)
    return count
@register.filter
def ccount(value,author):
    ct = Post.objects.filter(author__name=author,categories__name=value)
    return ct.count()
    
@register.filter
def check_can_pulish(author):
    try:
        author=Author.objects.get(user=author)
        # print(author.can_publish)
        return author.can_publish
    except:
        return False

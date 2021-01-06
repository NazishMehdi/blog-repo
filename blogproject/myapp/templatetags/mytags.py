from django import template
from myapp.models import Post
from django.db.models import Count
register=template.Library()#default template tag is total_posts
@register.simple_tag#using register variable we are accessing simple_tag
def total_posts():
    return Post.objects.count()#returns totak number of posts
@register.inclusion_tag ('myapp/latest_post.html')
def show_latest_posts(count=2):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}
@register.simple_tag
def get_most_commented_post(count=2):
    return Post.objects.annotate(total_comments=Count('comments')).order_by(-'total_comments')[:count]
    
from django.contrib import admin
from myapp.models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    l=['title','slug','author','body','publish','created','updated','status']
    prepopulated_fields={'slug':('title',)} #what ever typed in title gets affected in slug field. It is a dictionary and title should be list or tuple
    list_filter=('status','created','publish','author')
    search_fields=['title','publish']
    raw_id_fields=('author',) #author is single value tuple. identify author based on ID
    ordering=['status','publish']
class CommentAdmin(admin.ModelAdmin):
    l=['post','email','body','created','updated','active']
    list_filter=['active','created','updated']
    search_fields=['name','email','body']
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
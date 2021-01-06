from django.shortcuts import render,get_object_or_404
from myapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myapp.forms import EmailSentForm,CommentForm
from myapp.models import Comment
from django.core.mail import send_mail
from taggit.models import Tag
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()#to get all the records
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)#provided slug
        post_list=post_list.filter(tags__in=[tag])#list out all the post based on the condition that if the post are in tag object
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    d={'post_list':post_list,'tag':tag}
    return render(request,'myapp/post_list.html',d)
def post_detail_view(request,year,month,day,post):
    #if the record is available get that object else raise 404 error.It is available in django shortcuts
    post=get_object_or_404(Post,slug=post,publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    form=CommentForm()
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid:
            newcomment=form.save(commit=False)
            newcomment.post=post
            newcomment.save()
            csubmit=True
    d={'post':post,'form':form,'csubmit':csubmit,'comments':comments}
    return render(request,'myapp/post_detail.html',d)
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=EmailSentForm()
    if request.method=='POST':
        form=EmailSentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{0}[{1}] recomends you to read {2}'.format(cd['name'],cd['email'],post.title)
            message="Read the post at \n {0}\n {1} \n comments {2}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'nazish23mehdi@gmail.com',[cd['to']])
    d={'post':post,'form':form}
    return render(request, 'myapp/sharebymail.html',d)


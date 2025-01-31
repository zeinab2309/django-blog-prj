from django.contrib.admin.templatetags.admin_list import results
from django.http import  HttpResponse
from django.shortcuts import render,get_object_or_404 ,redirect
from django.template.context_processors import request
from django.views.generic import DetailView ,ListView

from .forms import TicketForm, CommentForm, SearchForm
from .models import *
#from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.


def index(request):

    return render(request, "blog/index.html")


# def post_list(request):
#     posts=Post.published.all()
#     paginator=Paginator(posts,2)
#     page_number=request.GET.get('page',1) #میگه در گت برو شماره صفحه رو پیدا کن اگر ب هر دلیلی پیدا نکردی مقدار پیشفرض 1 را بردار (از قابلیت های گت هست)
#     try:
#         posts=paginator.page(page_number)
#     except EmptyPage:
#         posts=paginator.page(paginator.num_pages) #اگر عدد ای دی بالا بود و وجود نداشت صفحه لیست اخر را نمایش بده
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context={
#         'posts':posts,
#     }
#     return render(request,"blog/list.html",context)

#----class base view----
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/list.html"



#ایدی ها ثابت نیستن
def post_detail(request , pk):
    post=get_object_or_404(Post,id=pk ,status=Post.Status.PUBLISHED)
    comments=post.comments.filter(active=True)
    form=CommentForm()
    context={
        'post':post,
        'form':form,
        'comments':comments

    }
    return render(request,"blog/detail.html",context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = "blog/detail.html"



def ticket(request):

    if request.method=="POST":
        form=TicketForm(request.POST)
        if form.is_valid():
            ticket_obj =Ticket.objects.create()
            cd=form.cleaned_data
            ticket_obj.message=cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")
    else:
        form=TicketForm()
    return render(request , "forms/ticket.html",{'form':form})

def post_comment(request, post_id):
    post=get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)#برای اینکه در دیتا بیس اول سیو نشه اول پست روش اضافه بشه بعد سیو بشه
        comment.post=post
        comment.save()
    context={
        'post':post,
        'form':form,
        'comment':comment

    }
    return render(request, "forms/comment.html", context)

def post_search(request):
    query=None
    esults=[]
    if 'query' in request.GET:
       form=SearchForm(data=request.GET)
       if form.is_valid():
           query=form.cleaned_data['query']
           results1=Post.published.filter(title__icontains=query)
           results2 = Post.published.filter(description__icontains=query)
           results=results1 | results2
       context={
           'query':query,
           'results':results
       }
    return render(request,'blog/search.html',context)
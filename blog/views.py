from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404 ,redirect
from django.views.generic import DetailView ,ListView
from .forms import TicketForm, CommentForm, SearchForm, CreatePostForm, UserRegisterForm
from .models import *
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import authenticate, login, logout


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
    post=get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
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
    results=[]
    if 'query' in request.GET:
       form=SearchForm(data=request.GET)
       if form.is_valid():
           query=form.cleaned_data['query']
           results1 = (Post.published.annotate(similarity=TrigramSimilarity('title',query))
                      .filter(similarity__gt=0.1)).order_by('-similarity')
           results2 = (Post.published.annotate(similarity=TrigramSimilarity('description',query))
                      .filter(similarity__gt=0.1)).order_by('-similarity')
           results=(results1 | results2).order_by('-similarity')
       context={
           'query':query,
           'results':results
       }
    return render(request,'blog/search.html',context)


@login_required
def profile(request):
    user=request.user
    posts=Post.published.filter(auther=user)
    return render(request, 'blog/profile.html', {'posts':posts})

@login_required
def create_post(request):
    if request.method=="POST":
        form=CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.auther=request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'],post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'],post=post)
            return redirect('blog:profile')
    else:
        form=CreatePostForm()
    return render(request, 'forms/create-post.html',{'form':form})

@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=="POST":
        post.delete()
        return redirect('blog:profile')
    return render(request,'forms/delete-post.html',{'post':post})

@login_required
def delete_image(request,image_id):
    image=get_object_or_404(Image,id=image_id)
    image.delete()
    return redirect('blog:profile')

@login_required
def edit_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.auther = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'forms/create-post.html', {'form': form, 'post':post})
#
# def user_login(request):
#     if request.method=="POST":
#         form= LoginForm(request.POST)
#         if form.is_valid():
#             cd=form.cleaned_data
#             user= authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return  redirect('blog:profile')
#                 else:
#                     return HttpResponse("شما نتوانستید وارد بشوید")
#     else:
#         form=LoginForm()
#     return render(request, 'forms/login.html', {'form':form})


def log_out(request):
    logout(request)
    return  redirect(request.META.get('HTTP_REFERER'))

def register(request):
    if request.method=='POST':
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user':user})
    else:
        form=UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})
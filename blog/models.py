from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from  django.urls import  reverse


#Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
# Create your models here.
class Post(models.Model):
    #برای وقتایی که میخواییم از یک انتخاب چند گزینه ای استفاده کنیم
    class Status(models.TextChoices):#کلاس برای وضعیت پست ایجاد کردیم که در چه حالتی هست
        DRAFT = "DF", 'Draft'
        PUBLISHED = "PB", 'Published'
        REJECTED = "RJ", 'Rejected'#برای رد شده

#یک سری فیلد مثل تایتل ما توش مقداری مینویسیم و میره یک سری فیلد مثل کلاس استاتوس ممکنه چند مقادیر مشخص داشته باشه ولی یک سری فیلد دیگه ممکن است از یک جدول دیگه باشه ک داریم استفاده میکنیم جدول یوزر نیاز داریم از خود جنگو استفاده میکنیمmany-to-one
#هر نویسنده در پست ها میتونه چند پست داشته باشه ولی هر پست متعلق به یک نویسنده هست
    #Relations
    auther=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_posts",verbose_name="نویسنده")
    #CASCADE-> اگر کاربری حذف شه تمام پست هاشم همراهش حذف میشه مثل پست اینستا ک اگر اکان حذف شه پست ها هم حذف میشن
    #data fileds
    title=models.CharField(max_length=250 ,verbose_name="موضوع")
    description=models.TextField(verbose_name="توضیحات")
    slug=models.SlugField(max_length=250 ,verbose_name="اسلاگ")
    #date
    publish=jmodels.jDateTimeField(default=timezone.now ,verbose_name="تاریخ انتشار")
    created=jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    #فیلد های انتخابی
    status=models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT ,verbose_name="وضعیت")
    #default ->برای وقتی این میذاریم ک ب عنوان پیش نویس هست تا وقتی ادمین اجازه ی انتشار را میدهد بعد انتشار پیدا میکند
    # objects=models.Manager()
    objects = jmodels.jManager()
    published=PublishedManager()
    #وارد shell میشویم
    class Meta:
        ordering=['-publish']
        indexes=[
            models.Index(fields=['-publish'])
        ]
        verbose_name="پست"
        verbose_name_plural = "پست ها"
    def __str__(self):
        return self.title

#بجای اینکه ادرس رو مشخص کنیم از این تابع استفاده میکنیم برای پستمون و ادرس اونو دقیق نمایش میده همچنین در قسمت ادمین یه مشاهده در وب گاه میاد ک خیلی راحت میتونیم اون پست رو در سایتمون ببینیم
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Ticket(models.Model):
    message=models.TextField(verbose_name="پیام")
    name=models.CharField(max_length=250 , verbose_name="نام")
    email=models.EmailField(verbose_name="ایمیل")
    phone=models.CharField(max_length=11,verbose_name="شماره تلفن")
    subject=models.CharField(max_length=250,verbose_name="موضوع")


    class Meta:
        verbose_name="تیکت"
        verbose_name_plural = "تیکت ها"
    def __str__(self):
        return self.subject

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments",verbose_name="پست")
    name=models.CharField(max_length=250,verbose_name="نام")
    body=models.TextField(verbose_name="متن کامنت")
    created=jmodels.jDateTimeField(auto_now_add=True)
    update=jmodels.jDateTimeField(auto_now=True)
    active=models.BooleanField(default=False)

    class Meta:
        ordering=['-created']
        indexes=[
            models.Index(fields=['-created'])
        ]
        verbose_name="کامنت"
        verbose_name_plural = "کامنت ها"
    def __str__(self):
        return f"{self.name}:{self.post}"

from django.db import models
from django.db.models import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from  django.urls import  reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify

#Managers ->میخواییم اونهایی که published هست را نمایش میده
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
    CATEGORY_CHOICES=(
        ('تکنولوژی','تکنولوژی'),
        ('زبان برنامه نویسی','زبان برنامه نویسی'),
        ('هوش مصنوعی','هوش مصنوعی'),
        ('بلاکچین','بلاکچین'),
        ('سایر','سایر')
    )

    #Relations
    auther=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_posts",verbose_name="نویسنده")
    #مدل هایی ک یک به چند هستند را از ForeignKey استفاده میکنیم
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
    reading_time=models.PositiveIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='سایر')

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

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage,path=img.image_file.storage, img.image_file.path
            storage.delete(path)
        super().delete(*args,**kwargs)


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


class Image(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", verbose_name="پست")
    image_file=ResizedImageField(upload_to="post_images/", size=[500,500], quality=75, crop=['middle','center'])
    title=models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description=models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created=jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created']
        indexes=[
            models.Index(fields=['-created'])
        ]
        verbose_name="تصویر"
        verbose_name_plural = "تصویر ها"
    def delete(self, *args, **kwargs):
        storage,path=self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args,**kwargs)

    def __str__(self):
        return self.title if self.title else "None"

class Account(models.Model):
    user=models.OneToOneField(User, related_name="account", on_delete=models.CASCADE )
    date_of_birth=jmodels.jDateTimeField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio=models.TextField(verbose_name=" بایو ", blank=True, null=True )
    photo=ResizedImageField(upload_to="account_images/", size=[500,500], quality=60, crop=['middle','center'],null=True, blank=True)
    job=models.CharField(max_length=250,verbose_name="شغل", blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name= "اکانت"
        verbose_name_plural="اکانت ها"
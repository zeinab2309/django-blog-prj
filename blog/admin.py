from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import *
# Register your models here.

#برای فارسی سازی پنل مدیریت میتونیم هم این ها رو برداریم و چون تو تنظیمات فارسی رو تعریف کردیم خودش هم میتونه فارسی کنه ب صورت خودکار با ترجمه شخصی خودش
admin.sites.AdminSite.site_header="پنل مدیریت جنگو"
admin.sites.AdminSite.site_title="پنل "
admin.sites.AdminSite.index_title="پنل مدیریت"

#این خط باعث میشود که مدل پست ک ایجاد کردیم در قسمت ادمین باشه و ب دلخواه ما ترتیبش باشه
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','auther','publish','status']
    ordering = ['title','publish']
    list_filter = ['status','auther',('publish',JDateFieldListFilter)]
    search_fields = ['title','description']
    raw_id_fields = ['auther']
    date_hierarchy = 'publish'
    prepopulated_fields = {"slug":['title']}#برای کلید فیلدی را که میخواییم خودکار تولید بشه مینویسم برای مقدار هم چیزی ک قراره اسلاگ ازش ساخته بشه ک تایتل هست
    list_editable = ['status']#میتونیم در قسمت سلکت ست ها ادیت کنیم بدون اینکه صفحه ادیت پست را باز کنیم فیلد دلخواه رو تغییر بدیم
    list_display_links = ['title','auther']#در حالت معمولی فقط روی اولین گزینه بزنیم صفحه ادیت رو میاره میتونیم ادیت کنیم برای بقیه از این استفاده میکنیم


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phone']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active',('created',JDateFieldListFilter),('update',JDateFieldListFilter)]
    search_fields = ['name','body']
    list_editable = ['active']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'title', 'created']


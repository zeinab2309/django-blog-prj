from  django.urls import path
from . import views
app_name="blog"

urlpatterns=[
    path('',views.index , name="index"),#یو ار ال مخصوص صفحه محصولات است
    #path('posts/', views.post_list, name="post_list"), #روی صفحه پست ها کلیک کنیم این یو ار ال را میاره
    path('posts/',views.PostListView.as_view() , name="post_list"),
    path('posts/<int:pk>/',views.PostDetailView.as_view() , name="post_detail"),#برای موقعی که روی یک پست بزنه ایدی جدا میده
    path('ticket',views.ticket , name="ticket"),

]



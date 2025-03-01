from  django.urls import path
from . import views
app_name="blog"

urlpatterns=[
    path('',views.index , name="index"),#یو ار ال مخصوص صفحه محصولات است
    #path('posts/', views.post_list, name="post_list"), #روی صفحه پست ها کلیک کنیم این یو ار ال را میاره
    path('posts/',views.PostListView.as_view() , name="post_list"),
    path('posts/<int:pk>/', views.post_detail, name="post_detail"),#برای موقعی که روی یک پست بزنه ایدی جدا میده
    path('posts/<int:post_id>/comment', views.post_comment, name="post_comment"),
    path('ticket', views.ticket, name="ticket"),
    path('search/',views.post_search, name="post_search"),
    path('profile/', views.profile, name="profile"),
    path('profile/create', views.create_post, name="create_post"),
    path('profile/create/<int:post_id>', views.edit_post, name="edit_post"),
    path('profile/delete_post/<int:post_id>', views.delete_post, name="delete_post"),
    path('profile/delete_image/<int:image_id>', views.delete_image, name="delete_image"),
    path('login', views.user_login,name="login")

]



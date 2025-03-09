from django.contrib.messages import success
from  django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name="blog"

urlpatterns=[
    path('',views.index , name="index"),
    #path('posts/', views.post_list, name="post_list"),
    path('posts/',views.PostListView.as_view() , name="post_list"),
    path('posts/<int:pk>/', views.post_detail, name="post_detail"),
    path('posts/<int:post_id>/comment', views.post_comment, name="post_comment"),
    path('ticket', views.ticket, name="ticket"),
    path('search/',views.post_search, name="post_search"),
    path('profile/', views.profile, name="profile"),
    path('profile/create', views.create_post, name="create_post"),
    path('profile/create/<int:post_id>', views.edit_post, name="edit_post"),
    path('profile/delete_post/<int:post_id>', views.delete_post, name="delete_post"),
    path('profile/delete_image/<int:image_id>', views.delete_image, name="delete_image"),
    # path('login', views.user_login,name="login"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('password-change/',auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('password-reset',auth_views.PasswordResetView.as_view(success_url='password-reset/done/'),name="password_reset"),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password-reset/complete'), name="password_reset_confirm"),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]



from django.urls import path
from . import views
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/newpost/', views.PostCreateView.as_view(), name='post_create'),

    path('post/<int:pk>/editpost/',
         views.PostUpdateView.as_view(), name='post_update'),

    path('post/<int:pk>/removepost/',
         views.PostDeleteView.as_view(), name='post_delete'),

    path('drafts/', views.DraftListView.as_view(), name='post_drafts'),
    path('post/<int:pk>/publish/', views.publish_post, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment, name='adding_comment'),

    path('comment/<int:pk>/approving/',
         views.approving_comment, name='approve_comment'),

    path('comment/<int:pk>/removing/',
         views.remove_comment, name='remove_comment'),
]

from django.shortcuts import redirect, render, get_object_or_404
from blog.models import Comments, Post
from blog.forms import PostForm, CommentsForm
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

########################################################################
# CBV FOR POSTS(post creating upodating deleting drafting)
#########################################################################


class AboutView(TemplateView):
    template_name = "blog/about.html"


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        # its kinda SQL query on the model POST.
        # returning objects like we did in FBV filtering it by
        # published_date__lte(<= lesser than equal to) timezone.now
        # so it filter by lets say the time is 17:00 it filters posts by time less than 17:00
        # and order it by -published_date
        # the dash before published_date is to make the post doesnt come from older to newer and rather
        # comes from new to old in a descending order
        # __lte is called lookups kinda stuff we use in SQL find it here more
        # https://docs.djangoproject.com/en/3.1/ref/models/lookups/
        # https://docs.djangoproject.com/en/3.1/howto/custom-lookups/
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

# we used @login_required for FBV but we can do that for CBV so we inherit LoginRequiredMixin
# which we import from django.contrib.auth.mixins

# it has two attributes login_url and redirect_field_name
# login_url defaults to settings.LOGIN_URL
# redirect_field_name is where we wanna redirect user after loging in


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'

    model = Post

    def get_queryset(self):
        # this time to see the draft list here we dont want the published_date cause we havent yet did it
        # so using lookups again  published_date__isnull=True.
        # this time we use __isnull = True which means as u know published date is gonna be null
        # and we are gonna order it by the create date descending like we did for post_list
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')


########################################################################
# FBV FOR COMMENTS AND PUBLISHING POST (comment approving  deleting)
#########################################################################

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentsForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def approving_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)


@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail', pk=post_pk)

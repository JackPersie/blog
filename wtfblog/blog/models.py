from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


# Model for Posting something on blog
class Post(models.Model):
    #  one user or multiple usersie the super user. thats why we are using auth.User
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

# published date can either be left empty or none or when published get the current date use the below method
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comment(self):
        return self.comments.filter(approved_comment=True)

    # after posting the blog returns to the blog

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


# Model for Commenting something on blog
class Comments(models.Model):
    # to post a comment, inherit the Post class u can either use blog.Post or just Post
    # reason for blog.Post is its more explicit ie clear and clean than implicit and the blog comes from the app name in app.py
    post = models.ForeignKey(
        'blog.Post', related_name='comments', on_delete=models.CASCADE)
    # random user without any need of credintials
    user = models.CharField(max_length=20)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())

    # this is not approved by default and it goes back to approve_comment() in Post where it only show approved_comment= True
    approved_comment = models.BooleanField(default=False)

    # for making approved_comment= True
    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_list')

    def __str__(self):
        return self.user

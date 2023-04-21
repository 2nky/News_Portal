from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        rating = 0.0
        for post in self.post_set.all():
            rating += post.rating * 3
            for comment in post.comment_set.all():
                rating += comment.rating

        for comment in Comment.objects.filter(user=self.user):
            rating += comment.rating

        self.rating = rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=30, default="", unique=True)

    def __str__(self):
        return f"{self.category_name}"


TYPES = [
    ("NW", "news"),
    ("AT", "article"),
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default="news")
    creation_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255, default="Новость часа")
    text = models.TextField(default="а мы уже пишем")
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text[0:124]
        text = text + "..."
        return text

    def __str__(self):
        return f"Пост: '{self.title}'"

    def get_absolute_url(self):
        return reverse("news_detail", args=[str(self.id)])


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default="")
    creation_time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):

        post_r = self.post_set.aggregate(PostRating=Sum("rating"))
        pr = 0
        pr += post_r.get("PostRating")

        comment_r = self.user.comment_set.aggregate(CommentRating=Sum("rating"))
        cr = 0
        cr += comment_r.get("CommentRating")

        self.author_rating = pr * 3 + cr
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    NEWS = "NE"
    ARTICLE = "AR"

    choices = (
        (NEWS, "Новость"),
        (ARTICLE, "Статья"),
    )

    category_type = models.CharField(max_length=2, choices=choices, default=ARTICLE)
    created = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if isinstance(self.text, str):  # проверка на то, что self.text является строкой
            return self.text[:64] if len(self.text) > 64 else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



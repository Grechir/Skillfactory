from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


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

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
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

    category_type = models.CharField(max_length=2, choices=choices, default=NEWS)
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

    def __str__(self):
        return f'{self.title.title()}: {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


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



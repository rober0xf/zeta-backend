from django.db import models
from django.utils import timezone
from django_prose_editor.fields import ProseEditorField

from apps.categories.models import Category


def blog_thumbnail_dir(instance, filename):
    return f"blog/{instance.title}/{filename}"


class Post(models.Model):
    # we will see the post in the get request if the post is published. by default they're draft
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    thumbnail = models.ImageField(upload_to=blog_thumbnail_dir, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)  # if we delete the category, we dont want the post to delete
    published = models.DateField(default=timezone.now)
    content = ProseEditorField(
        extensions={"Bold": True, "Italic": True, "BulletList": True, "Link": True},
        sanitize=True,
    )
    views = models.IntegerField(default=0, blank=True)
    status = models.CharField(max_length=10, choices=options, default="draft")
    objects = models.Manager()  # manager by default
    post_objects = PostObjects()  # our custom manager

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return self.title

    def get_view_count(self):
        views = ViewCount.objects.filter(post=self).count()
        return views


class ViewCount(models.Model):
    post = models.ForeignKey(Post, related_name="blogpost_view_count", on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return self.ip_address

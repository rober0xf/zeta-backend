from django.db import models
from django.utils import timezone
from apps.categories.models import Category
from django_prose_editor.fields import ProseEditorField


def blog_thumbnail_dir(instance, filename):
    return "blog/{0}/{1}".format(instance.title, filename)


class Post(models.Model):
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

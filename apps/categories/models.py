from django.db import models


# Create your models here.
class Category(models.Model):
    # visualize from django admin
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)  # for the url
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0, blank=True)

    # just return the name
    def __str__(self):
        return self.name

    def get_view_count(self):
        views = ViewCount.objects.filter(category=self).count()  # all the views count that are owner by the category model
        return views


class ViewCount(models.Model):
    category = models.ForeignKey(Category, related_name="category_view_count", on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address}"

from django.contrib import admin
from .models import Category


# add my category to the admin panel
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_display_links = ("name",)
    list_per_page = 25


admin.site.register(Category, CategoryAdmin)

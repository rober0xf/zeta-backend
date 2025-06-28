from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.categories.models import Category, ViewCount

from .models import Post
from .pagination import SmallPagination
from .serializers import PostListSerializer


class PostsListView(APIView):
    permission_classes = (permissions.AllowAny,)  # allow any to get request. it ends with , because its a tuple

    def get(self, request, format=None):
        if Post.objects.all().exists():
            posts = Post.objects.all()
            paginator = SmallPagination()
            results = paginator.paginate_queryset(posts, request)
            serializer = PostListSerializer(results, many=True)
            return paginator.get_paginated_response({"posts": serializer.data})  # we need to change the response to this function
        else:
            return Response({"error": "no posts found"}, status=status.HTTP_404_NOT_FOUND)


class ListPostByCategory(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if Post.objects.exists():
            slug = request.query_params.get("slug")  # get the slug from the url
            category = Category.objects.get(slug=slug)
            posts = Post.objects.order_by("-published").all()

            if not Category.objects.filter(parent=category).exists():  # it doesnt have a child, its a parent category
                posts = posts.filter(category=category)
            else:  # if it does have a child then we filter also the childs
                sub_categories = Category.objects.filter(parent=category)
                filtered_categories = list([category])
                filtered_categories.extend(sub_categories)  # add the sub categories to the filtered. we avoid using a for loop for performance

                filtered_categories_tuple = tuple(filtered_categories)
                posts = posts.filter(category__in=filtered_categories_tuple)
            paginator = SmallPagination()
            results = paginator.paginate_queryset(posts, request)
            serializer = PostListSerializer(results, many=True)
            return paginator.get_paginated_response({"posts": serializer.data})
        else:
            return Response({"error": "no posts found"}, status=status.HTTP_404_NOT_FOUND)


class PostDetailView(APIView):
    def get(self, request, post_slug):
        if Post.objects.filter(slug=post_slug).exists():
            post = Post.objects.get(slug=post_slug)
            serializer = PostListSerializer(post)

            address = request.META.get("HTTP_X_FORWARDED_FOR")
            if address:
                ip = address.split(",")[-1].strip()
            else:
                ip = request.META.get("REMOTE_ADDR")
            if not ViewCount.objects.filter(post=post, ip_address=ip):
                view = ViewCount(post=post, ip_address=ip)
                view.save()

            return Response({"post": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "post not found"}, status=status.HTTP_404_NOT_FOUND)

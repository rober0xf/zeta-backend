from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post
from .serializers import PostListSerializer
from .pagination import SmallPagination


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

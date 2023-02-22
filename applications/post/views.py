from rest_framework.viewsets import generics
from applications.post.models import Post, PostImage, Comment
from applications.post.serializers import PostSerializers, PostImageSerializer, CommentSerializer
from applications.feedback.serializers import RatingSerializer
from rest_framework.permissions import  IsAuthenticated, IsAuthenticatedOrReadOnly
from applications.post.permission import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters  import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from applications.feedback.models import Like, Rating


class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000



# class PostListCreateAPIView(generics.ListCreateAPIView):
#     # permission_classes = [IsOwner]
#     # queryset = Post.objects.all()
#     serializer_class = PostSerializers
#     pagination_class = CustomPagination

    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['owner','title']
    # search_fields = ['title']
    # ordering_fields = ['id']





# class PostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers


# class PostCreateAPIView(generics.CreateAPIView):
#     serializer_class = PostSerializers


# class PostUpdateAPIView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers


# class PostDeleteAPIView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers

# class PostDetailAPIView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers
# #     lookup_field = 'id'

# class PostListCreateAPIView(generics.ListCreateAPIView):
#     # permission_classes = [IsOwner, IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # queryset = queryset.filter(owner=5)
    #     filter_owner = self.request.query_params.get('owner')
    #     if filter_owner:
    #         queryset = queryset.filter(IsOwner=filter_owner)
    #     return queryset 


#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class PostDetailDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsOwner]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializers



class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsOwner]

    pagination_class = CustomPagination

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields  = ['owner','title']
    search_fields = ['title']
    ordering_fields = ['id', 'owner']


    @action(methods=['POST'], detail=True) # localhost:8000/api/v1/post/1/like/
    def like(self, request, pk, *args, **kwargs):
        user = request.user 
        like_obj, _ = Like.objects.get_or_create(owner=user,post_id=pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        status = 'liked'


        if not like_obj.is_like:
            status = 'unliked'

        return Response({'status': status})




    @action(methods=['POST'], detail=True)
    def rating(self,request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(owner=request.user, post_id=pk)
        rating_obj.rating = serializer.data['rating']
        rating_obj.save()
        print(serializer.data)
        return Response(serializer.data)



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class CreateImageAPIiew(generics.CreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(ViewSet):
    def list(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)




class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
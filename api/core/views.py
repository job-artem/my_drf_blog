from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from .serializers import PostSerializer, UserSerializer, TagSerializer, ContactSerailizer
from .models import Post
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import pagination
from taggit.models import Tag


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


# тестовое учебное апи
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerailizer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerailizer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail(f'От {name} | {subject}', message, from_email, ['amromashov@gmail.com'])
            return Response({"success": "Sent"})

# class FeedBackView(View):
#     def get(self, request, *args, **kwargs):
#         form = FeedBackForm()
#         return render(request, 'myblog/contact.html', context={
#             'form': form,
#             'title': 'Написать мне'
#         })
#
#     def post(self, request, *args, **kwargs):
#         form = FeedBackForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             from_email = form.cleaned_data['email']
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(f'От {name} | {subject}', message, from_email, ['amromashov@gmail.com'])
#             except BadHeaderError:
#                 return HttpResponse('Невалидный заголовок')
#             return HttpResponseRedirect('success')
#         return render(request, 'myblog/contact.html', context={
#             'form': form,
#         })


# class SuccessView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'myblog/success.html', context={
#             'title': 'Спасибо'
#         })

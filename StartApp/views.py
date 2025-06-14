from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .models import Category, Tag, Article
from django.views import View
from django.views.generic import DetailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer, CategorySerializer, TagSerializer, UserSerializer, UserRegisterSerializer
import requests

class UserListAPI(APIView):
    def get(self, req):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        external_api = requests.get('https://jsonplaceholder.typicode.com/users')
        external_data = external_api.json()
        data = {
            'local_users': serializer.data,
            'external_users': external_data
        }
        return Response(data)

class UserRegisterAPI(APIView):
    def post(self, req):
        serializer = UserRegisterSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Home(ListView):
    template_name = 'home.html'
    def get(self, req):
        articles = Article.objects.all()
        return render(req, self.template_name, {'articles': articles})

class Register(CreateView):
    template_name = 'register.html'

    def get(self, req):
        return render(req, self.template_name)
    
    def post(self, req):
        if req.method == 'POST':
            username = req.POST.get('username')
            email = req.POST.get('email')
            password = req.POST.get('password')

            user = User.objects.create_user(username=username, email=email, password=password)

            user.save()

            messages.success(req, 'Account created successfully! Please log in.')

            return redirect('login')
        
class ViewLogin(LoginView):
    template_name = 'login.html'
    def get(self, req):
        return render(req, self.template_name)

    def post(self, req):
        if req.user.is_authenticated:
            return redirect('/')
        if req.method == "POST":
            username = req.POST.get('username')
            password = req.POST.get('password')

            user = authenticate(req, username=username, password=password)

            if user is not None:
                login(req, user)
                return redirect('/')
            else:
                messages.error(req, 'please enter vaild username and password')
                return render(req, self.template_name)
    
class UserLogout(LogoutView):
    next_page = reverse_lazy('login')

class CreateArticle(CreateView):
    template_name = 'create_article.html'

    def get(self, req):
        tags = Tag.objects.all()
        categories = Category.objects.all()
        return render(req, self.template_name, {'tags': tags, 'categories': categories})

    def post(self, req):
        if req.method == "POST":
            title = req.POST.get('title')
            slug = req.POST.get('slug')
            description = req.POST.get('description')
            author = req.POST.get('author')
            image = req.FILES.get('image')
            category_id = req.POST.get('category')
            tag_id = req.POST.get('tag')
            tag = get_object_or_404(Tag, id=tag_id)
            category = get_object_or_404(Category, id=category_id)
            
            if not(title and slug and description and author and image and category and tag):
                  messages.error(req, 'Please fill all fields.')
           
            Article.objects.create(
                title=title,
                description=description,
                slug=slug,
                author=author,
                image=image,
                category=category,
                tag=tag
            )
        messages.success(req, "Article created successfully.")
        return redirect('/')
    
class CategoryArticle(View):
    template_name = 'category.html'

    def get(self, req):
        return render(req, self.template_name)
    
    def post(self, req):
        if req.method == "POST":
            name = req.POST.get('name')

            if name:
                Category.objects.create(name=name)
                return redirect('create_article')
            
            else:
                return render(req, self.template_name, {'error': 'Name field is required.'})
            
class TagCreate(View):
    template_name = 'tag.html'

    def get(self, req):
        return render(req, self.template_name)
    
    def post(self, req):
        if req.method == "POST":
            name = req.POST.get('name')

            if name:
                Tag.objects.create(name= name)
                return redirect('create_article')
            else:
                return render(req, self.template_name, {'error': 'Name field is required.'})

class ReadArticle(DetailView):
    model = Article
    template_name='read_article.html'
    context_object_name = 'article'

class EditArticle(View):
    template_name = 'edit_article.html'

    def get(self, req, id):
        article = get_object_or_404(Article, id=id)
        return render(req, self.template_name, {'article':article})
    
    def post(self, req, id):
        article = get_object_or_404(Article, id=id )
        article.title = req.POST.get('title')
        article.description = req.POST.get('description')
        article.slug = req.POST.get('slug')
        article.author = req.POST.get('author')
        article.image = req.FILES.get('image')
        
        if req.FILES.get('image'):
            article.image = req.FILES.get('image')
        article.save()

        return redirect('/')
    

class ArticleListAPI(APIView):
    def get(self, req):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        external_response = requests.get('https://jsonplaceholder.typicode.com/posts')
        external_data = external_response.json()
        data = {
            'local_articles': serializer.data,
            'external_articles': external_data
        }

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, req):
        serializer = ArticleSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailAPI(APIView):
    def get(self, req):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, req):
        serializer = CategorySerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def put(self, req, id):
        categories = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(categories, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        if category.article_set.exists():
            return Response(
                {'message': 'Cannot delete category. Articles are still linked to it.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        category.delete()
        return Response(
            {'message': 'Category deleted successfully.'},
            status=status.HTTP_200_OK
        )
    
    def patch(self, req, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class TagDetailAPI(APIView):
    def get(self, req):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)



class ArticleDetailAPI(APIView):
    def get(self, req, id):
        article = get_object_or_404(Article, id=id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, req, id):
        article = get_object_or_404(Article, id=id)
        serializer = ArticleSerializer(article, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, req, id):
        article = get_object_or_404(Article, id=id)
        serializer = ArticleSerializer(article, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, req, id):
        article = get_object_or_404(Article, id=id)
        article.delete()
        return Response({'messages': 'Article deleted successfully.'})
    

    def post(self, req):
        serializer = ArticleSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
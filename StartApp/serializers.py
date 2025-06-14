from rest_framework import serializers
from .models import Article, Category, Tag
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tag = TagSerializer()

    class Meta:
            model = Article
            fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    # articles = ArticleSerializer(source='article_set', many=True)
    article_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'article_count']

    def get_article_count(self, req):
        return req.article_set.count() 
    
class TagSerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = ['id', 'name', 'article_count']

    def get_article_count(self, req):
        return req.article_set.count() 
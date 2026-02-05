from rest_framework import serializers
from .models import Author
from .models import Book

class AuthorSerializer(serializers.ModelSerializer):
    # books=BookSerializer(many=True,read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'birth_year']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  
    author_id = serializers.IntegerField(write_only=True)  
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'published_year', 'author','author_id']
from rest_framework import viewsets
from .models import Author
from .models import Book
from .serializers import AuthorSerializer
from .serializers import BookSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .tasks import send_book_created_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
      queryset=Book.objects.all()
      serializer_class=BookSerializer
      filter_backends = [DjangoFilterBackend, filters.SearchFilter]
      filterset_fields = ['author', 'published_year']
      search_fields = ['title', 'isbn']  
      permission_classes = [IsAuthenticatedOrReadOnly] 

      def create(self,req,*args, **kwargs):
           res=super().create(req,*args, **kwargs)
           book_data=res.data
           author_name=book_data.get('author',{}).get('name','unknown')

           send_book_created_mail.delay(
                book_id=book_data['id'],
                book_title=book_data['title'],
                author_name=author_name
           )


           channel_layer = get_channel_layer()
           
           # what if DB transction rolls back here ,,then websocket messge will stillbe broadcasted even if book not created ? what to do here ?
           async_to_sync(channel_layer.group_send)(
                'book_notifications',
                {
                  'type':'book_created',
                  'book':res.data
                
                }
           )

           return res
      

      def destroy(self, request, *args, **kwargs):
           
           book=self.get_object()
           book_id=book.id,
           book_title=book.title

           response = super().destroy(request,*args, **kwargs)

           channel_layer=get_channel_layer()
           async_to_sync(channel_layer.group_send)(
                'book_notifications',
                {
                  'type':'book_deleted',
                  'book_id':book_id,
                  'message':f'book "{book_title}" has been deleted'

                }
           )
           return response






      
      

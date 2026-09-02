from rest_framework import viewsets
from books.models import Book
from books.serializers import BookSerializer
from books.permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides standard actions: list, create, retrieve, update, destroy.
    """
    
    # queryset defines where the data comes from (all books in the database)
    queryset = Book.objects.all()
    
    # serializer_class defines how the data is formatted (to JSON and back)
    serializer_class = BookSerializer

    # Assign the custom permission class
    permission_classes = (IsAdminOrReadOnly,)
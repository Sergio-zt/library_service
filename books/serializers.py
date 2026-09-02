from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book instances into JSON format and validates incoming data.
    """
    
    class Meta:
        # Specify the model to be serialized
        model = Book
        
        # Define which fields should be included in the API representation.
        # 'id' is automatically created by Django, we include it for referencing.
        fields = (
            'id', 
            'title', 
            'author', 
            'cover', 
            'inventory', 
            'daily_fee'
        )
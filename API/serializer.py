from rest_framework import serializers
from .models import Librarian, Member, Book, IssuedBook

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ['id', 'name', 'email', 'username']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            'id', 'first_name', 'last_name', 'gender', 'birthday',
            'email', 'phone', 'nic', 'address', 'postal_code',
            'city', 'province', 'fine', 'status'
        ]

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'published_date',
            'available', 'price', 'number_of_books'
        ]

class IssuedBookSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = IssuedBook
        fields = [
            'id', 'member', 'book', 'issue_date', 'due_date',
            'return_date', 'fine', 'status'
        ]

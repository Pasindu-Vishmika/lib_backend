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

    def validate(self, data):
        nic = data.get('nic', None)
        if nic:
            birthday, gender = self.context['request'].user.extract_birthday_and_gender_from_nic(nic)
            if data.get('birthday') != birthday:
                raise serializers.ValidationError({"birthday": "Birthday does not match NIC."})
            if data.get('gender') != gender:
                raise serializers.ValidationError({"gender": "Gender does not match NIC."})
        return data

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

    def create(self, validated_data):
        member_data = validated_data.pop('member')
        book_data = validated_data.pop('book')
        member = Member.objects.get(id=member_data['id'])
        book = Book.objects.get(id=book_data['id'])
        issued_book = IssuedBook.objects.create(member=member, book=book, **validated_data)
        return issued_book

    def update(self, instance, validated_data):
        member_data = validated_data.pop('member', None)
        book_data = validated_data.pop('book', None)
        
        if member_data:
            member = Member.objects.get(id=member_data['id'])
            instance.member = member

        if book_data:
            book = Book.objects.get(id=book_data['id'])
            instance.book = book

        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.return_date = validated_data.get('return_date', instance.return_date)
        instance.fine = validated_data.get('fine', instance.fine)
        instance.status = validated_data.get('status', instance.status)
        
        instance.save()
        return instance

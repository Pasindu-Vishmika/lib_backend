from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Member, IssuedBook
from .serializer import BookSerializer, MemberSerializer, IssuedBookSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = {
        'add-book': '/add-book/',
        'books': '/book-list/',
        'book': '/book/<str:pk>/',
        'updateBook': '/update-book/<str:pk>/',
        'deleteBook': '/delete-book/<str:pk>/',
        'issueBook': '/issue-book/<str:pk>/',
        'returnBook': '/return-book/<str:pk>/',
        'addMember': '/add-member/',
        'members': '/member-list/',
        'member': '/member/<str:pk>/',
        'updateMember': '/update-member/<str:pk>/',
        'deleteMember': '/delete-member/<str:pk>/',
    }
    return Response(routes)

@api_view(['POST'])
def addNewBook(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def searchBook(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['PUT'])
def updateBook(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBook(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def issueBook(request, pk):
    try:
        member = Member.objects.get(id=request.data.get('member_id'))
        book = Book.objects.get(id=pk)
    except (Member.DoesNotExist, Book.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    issued_book = IssuedBook(
        member=member,
        book=book,
        issue_date=request.data.get('issue_date'),
        due_date=request.data.get('due_date')
    )
    issued_book.save()
    serializer = IssuedBookSerializer(issued_book)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def returnBook(request, pk):
    try:
        issued_book = IssuedBook.objects.get(id=pk)
    except IssuedBook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    issued_book.return_date = request.data.get('return_date')
    issued_book.save()
    serializer = IssuedBookSerializer(issued_book)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addNewMember(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getMembers(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def searchMember(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MemberSerializer(member)
    return Response(serializer.data)

@api_view(['PUT'])
def updateMember(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MemberSerializer(member, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteMember(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    member.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def login(request):
    pass

def logout(request):
    pass

def sendEmail(request):
    pass

def memberProfile(request):
    pass

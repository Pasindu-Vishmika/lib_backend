from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login , logout
from .models import Book, Member, IssuedBook , Librarian
from .serializer import BookSerializer, MemberSerializer, IssuedBookSerializer , LibrarianSerializer

class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and isinstance(request.user, Librarian)

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
        'sendNotifications': '/send-notifications/',
    }
    return Response(routes)

@api_view(['POST'])
@permission_classes([IsLibrarian])
def addNewBook(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def searchBook(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsLibrarian])
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
@permission_classes([IsLibrarian])
def deleteBook(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsLibrarian])
def issueBook(request, pk):
    try:
        member = Member.objects.get(id=request.data.get('member_id'))
        book = Book.objects.get(id=pk)
    except (Member.DoesNotExist, Book.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if member.fine > 0:
        return Response({'detail': 'Member has outstanding fines and cannot borrow another book until fines are cleared.'}, status=status.HTTP_400_BAD_REQUEST)
    
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
@permission_classes([IsLibrarian])
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
@permission_classes([IsLibrarian])
def addNewMember(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsLibrarian])
def getMembers(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsLibrarian])
def searchMember(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = MemberSerializer(member)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsLibrarian])
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
@permission_classes([IsLibrarian])
def deleteMember(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    member.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getMemberFine(request):
    member = request.user
    if not isinstance(member, Member):
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    return Response({'fine': member.fine}, status=status.HTTP_200_OK)

"""
@api_view(['POST'])
@permission_classes([IsLibrarian])
def sendNotifications(request):
    message = request.data.get('message', 'This is a notification from the library.')
    members = Member.objects.all()

    for member in members:
        notification = Notification.objects.create(
            member=member,
            message=message
        )
        notification.send_email()

    return Response({'detail': 'Notifications sent to all members'}, status=status.HTTP_200_OK)"""

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authenticate without passing the request object
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        if isinstance(user, Librarian):
            serializer = LibrarianSerializer(user)
        else:
            serializer = MemberSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def logout(request):
    logout(request)
    return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

def sendEmail(request):
    pass

def memberProfile(request):
    pass

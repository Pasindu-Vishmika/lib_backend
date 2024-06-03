from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import BookSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = {
        'add-book': '/add-book/',
        'books': '/book-list/',
        'book': '/book/<str:pk>/',
        'updateBook': '/update-book/<str:pk>/',
        'deleteBook': '/delete-book/<str:pk>/',
        'IssueBook': '/issue-book/<str:pk>/',
        'returnBook': '/return-book/<str:pk>/',
        'addMember': '/add-member/',
        'members': '/member-list/',
        'member': '/member/<str:pk>/',
        'updateMember': '/update-member/<str:pk>/',
        'deleteMember': '/delete-member/<str:pk>/',
        
    }
    return Response(routes)

def addNewBook(request):
    pass

def getBooks(request):
    pass

@api_view(['GET'])
def searchBook(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response(serializer.data)

def updateBook(request, pk ):
    pass

def deleteBook(request , pk):
    pass

def issueBook(request , pk ):
    pass

def returnBook(request , pk ):
    pass

def addNewMember(request):
    pass

def getMembers(request):
    pass

def searchMember(request ,pk):
    pass

def updateMember(request , pk):
    pass

def deleteMember(request , pk ):
    pass

def login(request):
    pass

def logout(request):
    pass

def sendEmail(request):
    pass

def memberProfile(request):
    pass

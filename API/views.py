

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = {
        'books': '/book-list/',
        'book': '/book/<str:pk>/',
    }
    return Response(routes)

def addNewBook(request):
    pass

def getBooks(request):
    pass

def searchBook(request , pk):
    pass

def deleteBook(request , pk):
    pass

def updateBook(request, pk ):
    pass

def addNewMember(request):
    pass

def searchMember(request ,pk):
    pass

def deleteMember(request , pk ):
    pass

def updateMember(request , pk):
    pass

def issueBook(request , pk ):
    pass

def returnBook(request , pk ):
    pass

def login(request):
    pass

def logout(request):
    pass

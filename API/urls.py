from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),  
    
    path('add-book/', views.addNewBook, name='add-book'),
    path('book-list/', views.getBooks, name='book-list'),
    path('book/<str:pk>/', views.searchBook, name='book'),
    path('update-book/<str:pk>/', views.updateBook, name='update-book'),
    path('delete-book/<str:pk>/', views.deleteBook, name='delete-book'),
    path('issue-book/<str:pk>/', views.issueBook, name='issue-book'),
    path('return-book/<str:pk>/', views.returnBook, name='return-book'),
    path('add-member/', views.addNewMember, name='add-member'),
    path('member-list/', views.getMembers, name='member-list'),
    path('member/<str:pk>/', views.searchMember, name='member'),
    path('update-member/<str:pk>/', views.updateMember, name='update-member'),
    path('delete-member/<str:pk>/', views.deleteMember, name='delete-member'),
    path('member-fine/', views.getMemberFine, name='member-fine'),
]

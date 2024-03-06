from django.urls import path
from .views import *

urlpatterns =[
    # path('', home ),
    # path('student/',post_student),
    # path('update-student/<id>/',update_student),
    # path('update-students/<id>/',update_students),
    # path('delete-student/<id>/',delete_student),
    path('get-book/',GetBook),
    # path('add-book/',AddBook),
    # path('book-detail/<id>/',BookDetails),
    
    #APIView for student
    path('student/', StudentApi.as_view()),
    
    #APIView path for Books
    path('books/',Books.as_view()),
    path('register-user/', RegisterUser.as_view()),
    
    #Generic View for StudentGeneric
    path('gen-student/', StudentGeneric.as_view()),
    path('gen-student-UpdateDelete/<id>/',StudentGenericUpdateDelete.as_view()),
]
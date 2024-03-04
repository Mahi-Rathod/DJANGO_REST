from django.urls import path
from .views import *

urlpatterns =[
    path('', home ),
    path('student/',post_student),
    path('update-student/<id>/',update_student),
]
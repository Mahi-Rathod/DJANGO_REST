from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
#GET :- we fetch data from backend in frontend..
#POST:- we send data from frontend to backend
#PUT :- update data
#DELETE:- Delete Data


@api_view(['GET'])  #this only allow to POST Method
def home(request):
    Student_objects = Students.objects.all()
    serializers = StudentSerializers(Student_objects, many = True)

    return  Response({'status': 200, 'payload':serializers.data})

@api_view(['POST'])
def post_student(request):
    data = request.data
    print(data)
    serializer = StudentSerializers(data = request.data)


    if not serializer.is_valid():
        return Response({'Status':403, 'errors':serializer.errors, 'message':'Something went wrong'})
    serializer.save()
    return Response({"Status":200,"Payload":serializer.data, "message":"You sent"})

@api_view(['PUT'])     #in "PUT" for updating we had to send total data  what if we don't have track of all the data therefore we use "PATCH" method...
def update_student(request,id):
    try:
        student_obj = Students.objects.get(id=id)
        serializer = StudentSerializers(student_obj, data = request.data)

        if not serializer.is_valid():
            return Response({'Status':403, 'errors':serializer.errors, 'message':'Something went wrong'})
        

        serializer.save()
        return Response({"Status":200,"Payload":serializer.data, "message":"You sent"})
    except Exception as e:
        return Response({'Status': 403, 'message': "invalid id"})
    



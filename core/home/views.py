from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
#GET :- we fetch data from backend in frontend..
#POST:- we send data from frontend to backend
#PUT :- update data
#DELETE:- Delete Data

from rest_framework_simplejwt.tokens import RefreshToken

#generic views
from rest_framework import generics

class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    queryset = Students.objects.all()
    serializer_class= StudentSerializers

class StudentGenericUpdateDelete(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Students.objects.all()
    serializer_class= StudentSerializers
    lookup_field = 'id'



















#Class API View 
class RegisterUser(APIView):
    def get(self, request):
        user_obj = User.objects.all()
        serializer = UserSerializers(user_obj, many = True)
        return Response({'status':200, 'payload': serializer.data})
    
    def post(self, request):
        serializer = UserSerializers(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username = serializer.data['username'])
            
            # token_obj, _ = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({"status": 200, "Payload":serializer.data,'refresh':str(refresh), 'access':str(refresh.access_token), "message": "Registered Successfully.."})
        else:
            return Response({"status":403, "errors":serializer.errors, "message":"Something Went Wrong.."})




from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class StudentApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        Student_objects = Students.objects.all()
        serializers = StudentSerializers(Student_objects, many = True)
        print(request.user)
        return  Response({'status': 200, 'payload':serializers.data})
    
    def post(self,request):
        serializers = StudentSerializers(data=request.data)
        
        if serializers.is_valid():
            serializers.save()
            return Response({"status":200, "payload":serializers.data, "message":"Student added Successfully..."})
        else:
            return Response({"status":403, "errors":serializers.errors, "message":"Something Went Wrong.."})
    
    def put(self,request):
        try:
            student_obj = Students.objects.get(id=request.data['id'])  #we need to pass id from frontEnd
        except Exception as e:
            return Response({"status":400, "message":"Invalid ID"})
        
        serializer  = StudentSerializers(student_obj, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "payload":serializer.data, "message":"updated successfully"})
        else:
            return Response({"status":403,'errors':serializer.errors, 'message':'Something went wrong'})
        

    def patch(self,request):
        try:
            student_obj = Students.objects.get(id=request.data['id'])  #we need to pass id from frontEnd
        except Exception as e:
            return Response({"status":400, "message":"Invalid ID"})
        
        serializer  = StudentSerializers(student_obj, data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "payload":serializer.data, "message":"updated successfully"})
        else:
            return Response({"status":403,'errors':serializer.errors, 'message':'Something went wrong'})
        
        
    
    def delete(self,request):
        try:
            student_obj = Students.objects.get(id = request.data['id'])
        except Exception as e:
            return Response({"status":400, "message":"Invalid ID, Student with this id is not present in database.."})
        
        student_obj.delete()
        return Response({"status":200, "Message":"Deleted Successfully.."})



class Books(APIView):
    def get(self,request):
        bookObjects = Book.objects.all()
        serializer = BookSerializer(bookObjects, many = True)
        return Response({"status":200, "payload":serializer.data})
    
    def post(self, request):
        serializer = BookSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Status": 200, "Payload": serializer.data, "message": "Book added successfully"})
        else:
            return Response({"Status": 400, "errors": serializer.errors, "message": "Bad request"})

    def put(self, request):
        try:
            Book_obj = Book.objects.get(id = request.data['id'])
        except Exception as e:
            return Response({"status":403, "message":"Book With Given ID is not present in Database.."})
        
        serializer  = BookSerializer(Book_obj, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "payload":serializer.data, "message":"updated successfully.."})
        else:
            return Response({"status":403, "error":serializer.errors})
        
        
    def patch(self, request):
        try:
            Book_obj = Book.objects.get(id = request.data['id'])
        except Exception as e:
            return Response({"status":403, "message":"Book With Given ID is Not Present in Database.."})
        
        serializer = BookSerializer(Book_obj, data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "payload": serializer.data, "message":"updated successfully.."})
        else:
            return Response({"status":403, "error":serializer.errors})
        
    def delete(self, request):
        try:
            Book_obj = Book.objects.get(id = request.data['id'])
        except Exception as e:
            return Response({"status":"Book With Given ID is Not Present in Database.."})
        
        Book_obj.delete()
        return Response({"status":200, "message":"Book Deleted Successfully.."})



@api_view(['GET'])
def GetBook(request):
    bookObjects = Book.objects.all()
    serializers = BookSerializer(bookObjects, many = True)
    return Response({'status':200, 'payload':serializers.data})

# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def BookDetails(request, id):
#     try:
#         book = Book.objects.get(id = id)
#     except Book.DoesNotExist:
#         return Response({"Status": status.HTTP_404_NOT_FOUND, "message": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method =="GET":
#         serializers = BookSerializer(book)
#         return Response(serializers.data)
    
#     elif request.method == "PUT":
#         serializers = BookSerializer(book, data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response({"status":"200 OK", "payload":serializers.data})
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == "PATCH":
#         serializers = BookSerializer(book, data=request.data, partial = True)
#         if serializers.is_valid():
#             serializers.save()
#             return Response({"status":"200 OK", "payload":serializers.data})
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     elif request.method == 'DELETE':
#         book.delete()
#         return Response({"Status": status.HTTP_204_NO_CONTENT, "message": "Book deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
# @api_view(['POST'])
# def AddBook(request):
#     if request.method == 'POST':
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             print("i am here")
#             serializer.save()
#             return Response({"Status": 200, "Payload": serializer.data, "message": "Book added successfully"})
#         else:
#             return Response({"Status": 400, "errors": serializer.errors, "message": "Bad request"})



# """This Are For the Student Model"""

# @api_view(['GET'])  #this only allow to POST Method
# def home(request):
#     Student_objects = Students.objects.all()
#     serializers = StudentSerializers(Student_objects, many = True)

#     return  Response({'status': 200, 'payload':serializers.data})

# @api_view(['POST'])
# def post_student(request):
#     data = request.data
#     print(data)
#     serializer = StudentSerializers(data = request.data)


#     if not serializer.is_valid():
#         return Response({'Status':403, 'errors':serializer.errors, 'message':'Something went wrong'})
#     serializer.save()
#     return Response({"Status":200,"Payload":serializer.data, "message":"You sent"})

# @api_view(['PUT'])     #in "PUT" for updating we had to send total data  what if we don't have track of all the data therefore we use "PATCH" method...
# def update_student(request,id):
#     try:
#         student_obj = Students.objects.get(id=id)
#         serializer = StudentSerializers(student_obj, data = request.data)

#         if not serializer.is_valid():
#             return Response({'Status':403, 'errors':serializer.errors, 'message':'Something went wrong'})
        

#         serializer.save()
#         return Response({"Status":200,"Payload":serializer.data, "message":"You sent"})
#     except Exception as e:
#         return Response({'Status': 403, 'message': "invalid id"})
    
# @api_view(['PATCH'])
# def update_students(request, id):
#     try:
#         student_obj = Students.objects.get(id=id)
#     except Students.DoesNotExist:
#         return Response({'error':"invalid id"}, status=404)
    
#     if request.method == 'PATCH':
#         serializer = StudentSerializers(student_obj, data = request.data, partial = True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'PATCH Request for ID {id} processes successFully.'})
                
#         return Response({"Status":403,"error":serializer.errors})

# @api_view(['DELETE'])
# def delete_student(request, id):
#     try:
#         student_obj = Students.objects.get(id=id)
#         student_obj.delete()
#         return Response({"message":"Deleted Successfully.."})
        
#     except Exception as e:
#         print(e)
#         return Response({'status':403, 'message':'invalid id'})



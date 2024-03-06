from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from .helpers import *
class UserRegister(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status":200, "message":"OTP is Sent on Your number and email.."})
            else:
                return Response({"status":403, "error":serializer.errors})
        except Exception as e:
            print(e)
            return Response({"status":404, "error":"something went wrong"})

        
class VerifyOtp (APIView):
    def post (self, request):
        try:
            data = request.data
            user_obj = User.objects.get(phone = data.get('phone'))
            otp = data.get('otp')
            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({'status' : 200, 'message': 'your OTP is verified'})
            return Response({'status' : 403, 'message' : 'your OTP is wronng'})
        except Exception as e:
            print(e)
            return Response({'status' : 404, 'error' : 'something went wrong'}) 
        
    def patch(self,request):
        try:
            data = request.data
            if not User.objects.filter(phone = data.get('phone')).exists():
                return Response({'status' : 404, 'error' : 'Invalid Mobile Number.'})
            if send_otp_to_mobile(data.get('phone')):
                return Response({'status' : 200, 'error' : 'New OTP is sent on your Number.'})
            
            return Response({'status' : 404, 'error' : 'Try after few Second.'}) 
         
        except Exception as e:
            print(e)
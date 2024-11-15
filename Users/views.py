from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import REGAPISerializer,available_Courses_registrationserialization,liveclassSerializer,studentattendanceSerializer,ChangePasswordSerializer,ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from  rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from .models import User,available_Courses,studentatten
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import update_session_auth_hash
from rest_framework.generics import GenericAPIView
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import BadHeaderError
import socket
socket.getaddrinfo('127.0.0.1', 8000)

#Admin CRUD USers
#admin create user
@csrf_protect
@api_view(["POST"])
def tutor_register(request):
    if request.method=="POST":
       useremail= request.data.get("email")
       serializer=REGAPISerializer(data=request.data)
       if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#authenticated users to view users
@csrf_protect
@api_view(["GET"])
def view_tutor(request):
    if request.user.is_authenticated:
      post=User.objects.all()
      if request.method=="GET":
        serializer=REGAPISerializer(post, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    return Response(status = status.HTTP_401_UNAUTHORIZED)
# only admin can update users
@api_view(["PUT"])
@csrf_protect
@permission_classes([IsAdminUser])
def update_tutor(request,id):
    post=User.objects.get(id=id)
    if request.method=="PUT":
         serializer=REGAPISerializer(post,data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#only admin can delete users
@csrf_protect
@api_view(["DELETE"])
#@permission_classes([IsAdminUser])
def delete_tutor(request,id):
      if request.user.is_superuser:
        post=User.objects.get(id=id)
        if request.method=="DELETE":
          post.delete()
          return Response(status = status.HTTP_204_NO_CONTENT)
      return Response(status = status.HTTP_401_UNAUTHORIZED)


#userlogin
@csrf_protect
@api_view(['POST'])
def tutor_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        serializer=REGAPISerializer(data=request.data)
        user = None
       
        if not user:
            user = authenticate(username=username, password=password)
        if user.is_tutor:
           login(request, user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK,)
    return Response( status=status.HTTP_401_UNAUTHORIZED)
 

     
#admin login
@csrf_protect
@api_view(['POST'])
def admin_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if not user:
            user = authenticate(username=username, password=password)
        if user.is_superuser:
            login(request, user)
        else:
            return Response( status=status.HTTP_401_UNAUTHORIZED)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
#admin logout

@api_view(['POST'])
@csrf_protect
def admin_logout(request):
    if request.user.is_authenticated:
      if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            logout(request)
            return Response( status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status = status.HTTP_403_FORBIDDEN)

      

    #user logout

@api_view(['POST'])
@csrf_protect
def tutor_logout(request):
    if request.user.is_authenticated:
      if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            logout(request)
            return Response( status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status = status.HTTP_403_FORBIDDEN)


###course CRUD BY ADMIN
@csrf_protect
@api_view(["POST"])
#@permission_classes([IsAdminUser])
def addCourses(request):
    if request.user.is_superuser:
        if request.method=="POST":
         serializer=available_Courses_registrationserialization(data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status = status.HTTP_401_UNAUTHORIZED)


@csrf_protect
@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def getCourses(request):
    if request.user.is_authenticated:
      post=available_Courses.objects.all()
      if request.method=="GET":
        serializer=available_Courses_registrationserialization(post, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    return Response(status = status.HTTP_401_UNAUTHORIZED) 

@csrf_protect   
@api_view(["PUT"])
#@permission_classes([IsAdminUser])
def updateCourses(request,id):
    if request.user.is_superuser:
       post=available_Courses.objects.get(id=id)
       if request.method=="PUT":
         serializer=available_Courses_registrationserialization(post,data=request.data)
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status = status.HTTP_401_UNAUTHORIZED)

@csrf_protect
@api_view(["DELETE"])
#@permission_classes([IsAdminUser])
def deleteCourses(request,id):
    if request.user.is_superuser:
      post=available_Courses.objects.get(id=id)
      if request.method=="DELETE":
         post.delete()
         return Response(status = status.HTTP_204_NO_CONTENT)
    return Response(status = status.HTTP_401_UNAUTHORIZED)
   

    
# admin allow only tutor to add live class posts
@csrf_protect
@api_view(["POST"])
@permission_classes([IsAdminUser])
def tutorliveclasspost(request):
      if request.user.is_tutor: 
         if request.method =="POST":
            serializer = liveclassSerializer(data = request.data)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data,status = status.HTTP_201_CREATED)
      return Response(status = status.HTTP_401_UNAUTHORIZED)


# storing student attendance

@csrf_protect   
@api_view(["POST"])
#@permission_classes([IsAdminUser])
def atten(request):
    if request.user.is_student:
       student_email = request.data.get("student_email")
       if request.user.email == student_email:
          if request.method=="POST":
             serializer = studentattendanceSerializer(data = request.data)
             if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       return Response(status = status.HTTP_401_UNAUTHORIZED)
    return Response(status = status.HTTP_401_UNAUTHORIZED)


#tutor change password
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# password reset
class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        # Logic for sending the reset link email goes here
        if  email:
        # Use Django's PasswordResetForm to validate the email
            form = PasswordResetForm(data={"email": email})
            if form.is_valid():
            # Get the user associated with the email
               user = User.objects.filter(email=email).first()
            if user:
                try:
                    # Generate token and URL
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_url = f"{request.build_absolute_uri('/password-reset-confirm/')}?uid={uid}&token={token}"
               
                    # Send the email
                    form.save(
                        request=request,
                        use_https=True,
                        from_email="best9ja1@gmail.com",
                        email_template_name='email/password_reset_email.html',
                    )
                    return Response({"message": "Password reset link sent successfully."}, status=status.HTTP_200_OK)
                except BadHeaderError:
                    return Response({"error": "Invalid header found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordTokenCheck(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({'success': True, 'message': 'Token is valid'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
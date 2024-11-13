from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import REGAPISerializer,available_Courses_registrationserialization,liveclassSerializer,studentattendanceSerializer
from  rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from .models import User,available_Courses,studentattendance
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


def index(request):
    if request.method=="POST":
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        username=request.POST.get("username")
        email= request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        tutor=request.POST.get("tutor")
        student=request.POST.get("student")
        savetutor=User.objects.create(first_name=firstname, last_name=lastname, username=username,email=email,address=address,is_tutor=tutor,is_student=student)
        savetutor.set_password(password)
        savetutor.save()
    return render(request, "index.html")
#Admin CRUD USers
#admin create user
@api_view(["POST"])
def tutor_register(request):
    if request.method=="POST":
        """
        firstname=request.data.get("first_name")
        lastname=request.data.get("last_name")
        username=request.data.get("username")
        email= request.data.get("email")
        password=request.data.get("password")
        address=request.data.get("address")
        tutor=request.data.get("is_tutor")
        student=request.data.get("is_student")
        """
        serializer=REGAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#authenticated users to view users
@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def view_tutor(request):
    if request.user.is_authenticated:
      post=User.objects.all()
      if request.method=="GET":
        serializer=REGAPISerializer(post, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    return Response(status = status.HTTP_401_UNAUTHORIZED)
# only admin can update users
@api_view(["PUT"])
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
@api_view(['POST'])
def tutor_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        serializer=REGAPISerializer(data=request.data)
        user = None
       
        if not user:
            user = authenticate(username=username, password=password)
        if user.is_authenticated:
       # if user.is_tutor or user.is_student:
           login(request, user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK,)
    return Response( status=status.HTTP_401_UNAUTHORIZED)
 

     
#admin login
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
      

    #user logout
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def tutor_logout(request):
    if request.user.is_authenticated:
      if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response( status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status = status.HTTP_403_FORBIDDEN)


###course CRUD BY ADMIN

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

@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def getCourses(request):
    if request.user.is_authenticated:
      post=available_Courses.objects.all()
      if request.method=="GET":
        serializer=available_Courses_registrationserialization(post, many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    return Response(status = status.HTTP_401_UNAUTHORIZED)
    
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

@api_view(["POST"])
#@permission_classes([IsAdminUser])
def attendance(request):
      if request.user.is_student: 
         if request.method =="POST":
            student_email = request.data.get("student_email")
            #if the person signing attendance email is correct then
            if request.user.email == student_email:
               serializer = studentattendanceSerializer(data = request.data)
               if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data,status = status.HTTP_201_CREATED)
            return Response(status = status.HTTP_401_UNAUTHORIZED)
      return Response(status = status.HTTP_401_UNAUTHORIZED)

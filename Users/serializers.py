from rest_framework import serializers
from .models import User,available_Courses,liveclass,studentattendance

class REGAPISerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id","first_name","last_name","username","email","password","address","is_active","is_student","is_staff","is_tutor","is_superuser",)
     

class available_Courses_registrationserialization(serializers.ModelSerializer):
    class Meta:
        model=available_Courses
        fields=("id","title","slug","tutor",)


class liveclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = liveclass
        fields = ("class_name","class_description","class_link",)

# student attendance

class studentattendanceSerializer(serializers.ModelSerializer):
      class Meta:
          model =studentattendance
          fields =("student_email",)
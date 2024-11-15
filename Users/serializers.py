from rest_framework import serializers
from .models import User,available_Courses,liveclass,studentatten
from django.contrib.auth.password_validation import validate_password

class REGAPISerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model=User
        fields=("id","first_name","last_name","username","email","password","address","is_active","is_student","is_staff","is_tutor","is_superuser",)
     
    def create(self, validated_data):
        user = super(REGAPISerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class available_Courses_registrationserialization(serializers.ModelSerializer):
    class Meta:
        model=available_Courses
        fields=("id","title","slug","author",)


class liveclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = liveclass
        fields = ("class_name","class_description","class_link",)

# student attendance

class studentattendanceSerializer(serializers.ModelSerializer):
      class Meta:
          model =studentatten
          fields =("student_email","course_code","course_name","status",)
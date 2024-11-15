from rest_framework import serializers
from .models import User,available_Courses,liveclass,studentatten
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

#Reset password 
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('There is no user with this email address.')
        return data

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data.get('uidb64')))
            user = User.objects.get(id=uid)
            if not PasswordResetTokenGenerator().check_token(user, data.get('token')):
                raise serializers.ValidationError('The token is invalid or expired.')
            return data
        except Exception:
            raise serializers.ValidationError('The reset link is invalid.')

    def save(self, **kwargs):
        password = self.validated_data.get('password')
        uid = force_str(urlsafe_base64_decode(self.validated_data.get('uidb64')))
        user = User.objects.get(id=uid)
        user.set_password(password)
        user.save()


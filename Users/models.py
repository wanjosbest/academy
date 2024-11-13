from django.db import models
from django.contrib.auth.models import AbstractUser



#tutor register
class User(AbstractUser):
    
    email = models.EmailField(null =True, unique=True, max_length=100)
    address=models.CharField(max_length=300,null=True,blank=True)
    is_tutor=models.BooleanField(verbose_name="Tutor Status",null=True,default=True)
    # include this for a while
    is_student = models.BooleanField(verbose_name="Student Status",null=True)

    class Meta:
        verbose_name="Users"
        verbose_name_plural="Users"

    def __str__(self):
        return self.username
    

    
## add courses
class available_Courses(models.Model):
    author = models.ForeignKey(User, related_name="tutoraddcourse",on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=30,null=True)
    slug=models.SlugField(max_length=20,null=True)

    class Meta:
        verbose_name="available_Courses"
        verbose_name_plural="available Courses"
        
    def __str__(self):
        return self.title


    
#tutor to add live classes

class liveclass(models.Model):
   #  course = models.ForeignKey(available_Courses, related_name="liveclasscourse",on_delete=models.CASCADE,null=True)
     class_name=models.CharField(max_length=100,null=True,blank=False)
     class_description=models.TextField(max_length=1000,verbose_name="About the Live Class",null=True)
     class_link=models.CharField(max_length=255,unique=True,null=True,blank=False)
     def __str__(self):
         return self.class_name
     
#student attendance 

class studentattendance(models.Model):
    student_email=models.EmailField(max_length=100, unique=True,null=True, verbose_name ="Student Email") 
    course_code = models.ForeignKey(available_Courses, related_name="courseattendance",on_delete=models.CASCADE,null=True)
    course_name = models.CharField(max_length = 50, null =True, verbose_name="Attendance Course Name")
    status = models.CharField(max_length=10,choices=(('P','PRESENT'),('A','ABSENT')),default='PRESENT')
    entry_time = models.DateTimeField( null=True, auto_now_add = True, auto_now = False,blank=True)

    def __str__(self):
       return self.course_name
    
    class Meta:
        verbose_name="studentattendance"
        verbose_name_plural="Student Attendance"
   
  
   
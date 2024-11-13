from django.urls import path
from .import views


urlpatterns =[
    
     path("api/admin-login/",views.admin_login, name="admin_login"),
     path("api/tutor-login/",views.tutor_login, name="tutor_login"),
    
     path("api/tutor-logout/",views.tutor_logout, name="tutor-logout"),
     #ADMIN CRUD USERS
     path("api/tutor-register/",views.tutor_register, name="tutor_register"),
     path("api/view-tutor/",views.view_tutor, name="view_tutor"),
     path("api/update-tutor/<str:id>/",views.update_tutor, name="update_user"),
     path("api/delete-tutor/<str:id>/",views.delete_tutor, name="delete_user"),
     #admin CRUD
     path("api/addcourse/",views.addCourses, name="addcourse"),
     path("api/getcourse/",views.getCourses, name="getcourse"),
     path("api/updatecourse/<str:id>/",views.updateCourses, name="updatecourse"),
     path("api/deletecourse/<str:id>/",views.deleteCourses, name="deletecourse"),
     #end ADMIN CRUD
     path("", views.index, name="index"),
     # allow only tutor to add live class
     path("api/addliveclasspost/", views.tutorliveclasspost, name = "tutorliveclass"),

     # attendance
     path("api/student-attendance/",views.attendance, name="studentattendance"),
]
from django.urls import path
from .import views
from .views import RequestPasswordResetEmail, PasswordTokenCheck, SetNewPasswordView


urlpatterns =[
    
     path("api/admin-login/",views.admin_login, name="admin_login"),
     path("api/admin-logout/",views.admin_logout, name="admin_logout"),
     path("api/tutor-login/",views.tutor_login, name="tutor_login"),
    
     path("api/tutor-logout/",views.tutor_logout, name="tutor-logout"),
     #ADMIN CRUD Tutor
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

     # allow only tutor to add live class
     path("api/addliveclasspost/", views.tutorliveclasspost, name = "tutorliveclass"),

     # attendance
     path("api/student-attendance/",views.atten, name="studentattendance"),
     # password change
     path('api/change-password/', views.change_password, name='change_password'),

     #password reset
     path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
     path('password-reset-confirm/<uidb64>/<token>/', PasswordTokenCheck.as_view(), name='password-reset-confirm'),
     path('password-reset-complete/', SetNewPasswordView.as_view(), name='password-reset-complete'),

]
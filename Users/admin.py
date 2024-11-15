from django.contrib import admin
from .models import User,available_Courses,liveclass,studentatten

admin.site.register(User)

class available_CoursesAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("title",)}
admin.site.register(available_Courses,available_CoursesAdmin)


admin.site.register(liveclass)
admin.site.register(studentatten)

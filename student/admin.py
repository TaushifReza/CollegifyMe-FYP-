from django.contrib import admin

from student.models import StudentProfile


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name")
    ordering = ("-user",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(StudentProfile, StudentProfileAdmin)

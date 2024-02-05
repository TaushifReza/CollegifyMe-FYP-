from django.contrib import admin

from college.models import CollegeProfile


class CollegeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "college_name")
    ordering = ("-user",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(CollegeProfile, CollegeProfileAdmin)

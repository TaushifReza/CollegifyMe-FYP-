from django.contrib import admin

from student.models import StudentProfile, StudentEducation, StudentFriends


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name")
    ordering = ("-user",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(StudentEducation)
class StudentEducationAdmin(admin.ModelAdmin):
    list_display = ("user", "level_of_education", "degree_name", "college_name")
    ordering = ("-end_date",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(StudentFriends)
class StudentFriendsAdmin(admin.ModelAdmin):
    list_display = (
        "get_student_email",
        "get_friend_email",
        "status",
        "send_date",
        "accept_date",
    )
    ordering = (
        "-accept_request",
        "-request_send",
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def get_student_email(self, obj):
        return obj.student.user.email if obj.student.user.email else "N/A"

    get_student_email.short_description = "Student Email"

    def get_friend_email(self, obj):
        return obj.friend.user.email if obj.friend.user.email else "N/A"

    def send_date(self, obj):
        return obj.request_send.strftime("%Y-%m-%d")

    send_date.short_description = "Send Date"

    def accept_date(self, obj):
        if obj.accept_request:
            return obj.accept_request.strftime("%Y-%m-%d")
        else:
            return "N/A"

    accept_date.short_description = "Accept Date"

    get_friend_email.short_description = "Friend Email"

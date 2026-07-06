from django.contrib import admin
from .models import Department, Course, Student, Enrollment
# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')
    search_fields = ('name', 'code', 'department__name')
    list_filter = ('department',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_no', 'email', 'department', 'enrollment_year')
    search_fields = ('name', 'reg_no', 'email', 'department__name')
    list_filter = ('department', 'enrollment_year')

admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Enrollment)
admin.site.register(Department)
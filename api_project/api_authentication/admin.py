from django.contrib import admin
from api_authentication.models import CustomUser, Teacher


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'patronymic', 
                    'email', 'phone_number', 'role', 'date_joined')
    list_filter = ('role', 'date_joined')
    search_fields = ('^username', '^last_name', '^first_name', 
                     '^email', '^phone_number')
    
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'education', 'experience', 
                    'course_count', 'certificate_count')
    search_fields = ('^username', 'full_name__icontains')
    
    def certificate_count(self, obj):
        return obj.certificates.count()
    certificate_count.short_description = 'Certificate count'
    
    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Course count'

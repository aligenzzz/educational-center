from django.contrib import admin
from api_product.models import (Certificate, Article, CourseCategory, Course, Discount,
                                Review, FaqCategory, Faq, Application)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    search_fields = ('techer__icontains', )
    
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date')
    list_filter = ('creation_date', )
    search_fields = ('^title', )
    

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'study_hours', 'price_for_one', 'price_for_many',
                    'course_category')
    list_filter = ('study_hours', 'price_for_one', 'price_for_many',
                    'course_category')
    search_fields = ('^name', )
    
    def teacher_count(self, obj):
        return obj.teachers.count()
    teacher_count.short_description = 'Teacher count'
    
    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Student count'


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('percent', 'description')
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'course', 'creation_date')
    list_filter = ('creation_date', )
    search_fields = ('^author', '^course')


@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'faq_category')
    list_filter = ('faq_category', )
    search_fields = ('^question', )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone_number', 'email', 
                    'start_date', 'course')
    list_filter = ('start_date', 'course')
    search_fields = ('^surname', '^course')

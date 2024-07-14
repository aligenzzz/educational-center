from rest_framework import serializers
from .models import (TeacherInfo, Certificate, Article, CourseCategory, Course,
                     Discount, Review, FaqCategory, Faq, Application)
from api_authentication.models import User

class TeacherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherInfo
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d'])

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'




class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(queryset=TeacherInfo.objects.all(), many=True)
    students = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    course_category = serializers.PrimaryKeyRelatedField(queryset=CourseCategory.objects.all())

    class Meta:
        model = Course
        fields = '__all__'
        
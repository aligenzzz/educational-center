from rest_framework import serializers
from .models import (TeacherInfo, Certificate, Article, CourseCategory, Course,
                     Discount, Review, FaqCategory, Faq, Application)
from api_authentication.models import User


class TeacherInfoSerializer(serializers.ModelSerializer):   
    class Meta:
        model = TeacherInfo
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.photo:
            representation['photo'] = request.build_absolute_uri(instance.photo.url)
        else:
            representation['photo'] = None

        return representation
    
    def update(self, instance, validated_data):        
        instance.photo = validated_data.get('photo', instance.photo)
        instance.education = validated_data.get('education', instance.education)
        instance.experience = validated_data.get('experience', instance.experience)

        instance.save()
        
        return instance


class CertificateSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=TeacherInfo.objects.all())
    
    class Meta:
        model = Certificate
        fields = '__all__'
               
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.file:
            representation['file'] = request.build_absolute_uri(instance.file.url)
        else:
            representation['file'] = None

        return representation
    
    def create(self, validated_data):
        try:
            return Certificate.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e)) 
        
    def delete(self, instance):
        try:
            instance.delete()  
        except Exception as e:
            raise serializers.ValidationError(str(e))


class ArticleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Article
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        else:
            representation['image'] = None

        return representation


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'creation_date': {'read_only': True}
        }
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = {
            'id': instance.course.id,
            'name': instance.course.name,
            'category': instance.course.course_category.id
        }    
        return representation
    
    def create(self, validated_data):
        try:
            return Review.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e)) 


class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    faq_category = FaqCategorySerializer()
    
    class Meta:
        model = Faq
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = Application
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = {
            'id': instance.course.id,
            'name': instance.course.name,
            'category': instance.course.course_category.id
        }    
        return representation
    
    def create(self, validated_data):
        try:
            return Application.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))


class CourseSerializer(serializers.ModelSerializer):
    course_category = CourseCategorySerializer()
    
    class Meta:
        model = Course
        fields = '__all__'
         
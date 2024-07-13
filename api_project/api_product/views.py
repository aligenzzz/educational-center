from rest_framework import viewsets
from .models import (TeacherInfo, Certificate, Article, CourseCategory, Course,
                     Discount, Review, FaqCategory, Faq, Application)
from .serializers import (TeacherInfoSerializer, CertificateSerializer, ArticleSerializer,
                          CourseCategorySerializer, CourseSerializer, DiscountSerializer,
                          ReviewSerializer, FaqCategorySerializer, FaqSerializer, ApplicationSerializer)


class TeacherInfoViewSet(viewsets.ModelViewSet):
    queryset = TeacherInfo.objects.all()
    serializer_class = TeacherInfoSerializer
    

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    

class CourseCategoryViewSet(viewsets.ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
class FaqCategoryViewSet(viewsets.ModelViewSet):
    queryset = FaqCategory.objects.all()
    serializer_class = FaqCategorySerializer
    
    
class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    
    
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    
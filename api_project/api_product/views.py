from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from api_authentication.permissions import IsAdminOrOwnerTeacher
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import (TeacherInfo, Certificate, Article, CourseCategory, Course,
                     Discount, Review, FaqCategory, Faq, Application)
from .serializers import (TeacherInfoSerializer, CertificateSerializer, ArticleSerializer,
                          CourseCategorySerializer, CourseSerializer, DiscountSerializer,
                          ReviewSerializer, FaqCategorySerializer, FaqSerializer, ApplicationSerializer)


class TeacherInfoViewSet(viewsets.GenericViewSet):
    authentication_classes=[JWTAuthentication]
    queryset = TeacherInfo.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrOwnerTeacher]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        tags=['TeacherInfo'],
        responses={
            200: TeacherInfoSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TeacherInfoSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['TeacherInfo'],
        responses={
            200: TeacherInfoSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        teacher_info = self.get_object()
        serializer = TeacherInfoSerializer(teacher_info, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['TeacherInfo'],
        request_body=TeacherInfoSerializer,
        responses={
            200: openapi.Response(
                description='TeacherInfo was updated',
                schema=TeacherInfoSerializer,
            ),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
        },
    )
    def update(self, request, pk=None):
        teacher = self.get_object()
        serializer = TeacherInfoSerializer(teacher, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['TeacherInfo'],
        request_body=TeacherInfoSerializer,
        responses={
            200: openapi.Response(
                description='TeacherInfo was updated',
                schema=TeacherInfoSerializer,
            ),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
        },
    )
    def partial_update(self, request, pk=None):
        teacher = self.get_object()
        serializer = TeacherInfoSerializer(teacher, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CertificateViewSet(viewsets.GenericViewSet):
    authentication_classes=[JWTAuthentication]
    queryset = Certificate.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrOwnerTeacher]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        tags=['Certificates'],
        responses={
            200: CertificateSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CertificateSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Certificates'],
        responses={
            200: CertificateSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        certificate = self.get_object()
        serializer = CertificateSerializer(certificate, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Certificates'],
        request_body=CertificateSerializer,
        responses={
            201: openapi.Response(
                description='Certificate was created',
                schema=CertificateSerializer,
            ),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Forbidden',
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = CertificateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Certificates'],
        responses={
            204: 'Certificate was deleted',
            404: 'Not found',
            401: 'Unauthorized',
            403: 'Forbidden',
        },
    )
    def destroy(self, request, pk=None):
        certificate = self.get_object()
        serializer = CertificateSerializer()
        try:
            serializer.delete(certificate)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]  
    queryset = Article.objects.all()
    
    @swagger_auto_schema(
        tags=['Articles'],
        responses={
            200: ArticleSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ArticleSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Articles'],
        responses={
            200: ArticleSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        article = self.get_object()
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)


class CourseCategoryViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = CourseCategory.objects.all()
    
    @swagger_auto_schema(
        tags=['CourseCategories'],
        responses={
            200: CourseCategorySerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['CourseCategories'],
        responses={
            200: CourseCategorySerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        course_category = self.get_object()
        serializer = CourseCategorySerializer(course_category)
        return Response(serializer.data)


class DiscountViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = Discount.objects.all()
    
    @swagger_auto_schema(
        tags=['Discounts'],
        responses={
            200: DiscountSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DiscountSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Discounts'],
        responses={
            200: DiscountSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        discount = self.get_object()
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)
    
    
class ReviewViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = Review.objects.all()
    
    @swagger_auto_schema(
        tags=['Reviews'],
        responses={
            200: ReviewSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Reviews'],
        responses={
            200: ReviewSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        review = self.get_object()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Reviews'],
        request_body=ReviewSerializer,
        responses={
            201: openapi.Response(
                description='Review was created',
                schema=ReviewSerializer,
            ),
            400: 'Bad request',
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class FaqCategoryViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = FaqCategory.objects.all()
    
    @swagger_auto_schema(
        tags=['FaqCategories'],
        responses={
            200: FaqCategorySerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = FaqCategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['FaqCategories'],
        responses={
            200: FaqCategorySerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        faq_category = self.get_object()
        serializer = FaqCategorySerializer(faq_category)
        return Response(serializer.data)
    
    
class FaqViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = Faq.objects.all()
    
    @swagger_auto_schema(
        tags=['Faqs'],
        responses={
            200: FaqSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = FaqSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Faqs'],
        responses={
            200: FaqSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        faq = self.get_object()
        serializer = FaqSerializer(faq)
        return Response(serializer.data)
    
    
class ApplicationViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = Application.objects.all()
    
    @swagger_auto_schema(
        tags=['Applications'],
        responses={
            200: ApplicationSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ApplicationSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Applications'],
        responses={
            200: ApplicationSerializer,
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Applications'],
        request_body=ApplicationSerializer,
        responses={
            201: openapi.Response(
                description='Application was created',
                schema=ApplicationSerializer,
            ),
            400: 'Bad request',
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseViewSet(viewsets.GenericViewSet):
    authentication_classes=[]
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    
    @swagger_auto_schema(
        tags=['Courses'],
        responses={
            200: CourseSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=['Courses'],
        responses={
            200: CourseSerializer(),
            404: 'Not found',
        },
    )
    def retrieve(self, request, pk=None):
        course = self.get_object()
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
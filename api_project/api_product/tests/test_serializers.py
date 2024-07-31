import uuid

from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models.signals import m2m_changed
from django.test import RequestFactory
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from api_product.models import TeacherInfo, Certificate, Article, CourseCategory, Discount, Review, Course, FaqCategory, Faq, Application, Course
from api_authentication.models import User
from api_product.serializers import TeacherInfoSerializer, CertificateSerializer, ArticleSerializer, CourseCategorySerializer, DiscountSerializer, ReviewSerializer, FaqCategorySerializer, FaqSerializer, ApplicationSerializer, CourseSerializer
from api_product.forms import CourseForm
from api_product.signals import validate_students


class TeacherInfoSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='complexpassword',
            first_name='Test',
            last_name='User',
            role='teacher'
        )
        self.teacher_info = TeacherInfo.objects.create(
            user=self.user,
            education='PhD in Computer Science',
            experience='10 years of experience'
        )
        self.factory = RequestFactory()

    def test_serializer_valid(self):
        serializer = TeacherInfoSerializer(instance=self.teacher_info)
        data = serializer.data
        self.assertEqual(data['user'], str(self.user.id))
        self.assertEqual(data['education'], self.teacher_info.education)
        self.assertEqual(data['experience'], self.teacher_info.experience)

    def test_serializer_photo_url(self):
        self.teacher_info.photo = ContentFile(b'file_content', 'photo.jpg')
        self.teacher_info.save()
        request = self.factory.get('/api/teacher-info/')
        serializer = TeacherInfoSerializer(instance=self.teacher_info, context={'request': request})
        data = serializer.data
        self.assertIn('photo', data)
        self.assertTrue(data['photo'].startswith('http://testserver'))

    def test_serializer_update(self):
        updated_data = {
            'education': 'Updated Education',
            'experience': 'Updated Experience'
        }
        serializer = TeacherInfoSerializer(instance=self.teacher_info, data=updated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_teacher_info = serializer.save()
        self.assertEqual(updated_teacher_info.education, 'Updated Education')
        self.assertEqual(updated_teacher_info.experience, 'Updated Experience')

    def test_serializer_invalid_data(self):
        invalid_data = {
            'user': 'invalid_user_id',
            'education': '',
            'experience': ''
        }
        serializer = TeacherInfoSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class CertificateSerializerTest(APITestCase):
    def setUp(self):
        self.teacher_info = TeacherInfo.objects.create(
            user=User.objects.create_user(
                username='testuser',
                password='complexpassword',
                first_name='Test',
                last_name='User',
                role='teacher'
            ),
            education='PhD in Computer Science',
            experience='10 years of experience'
        )
        self.certificate = Certificate.objects.create(
            file=ContentFile(b'file_content', 'certificate.pdf'),
            teacher=self.teacher_info
        )
        self.factory = RequestFactory()

    def test_serializer_valid(self):
        request = self.factory.get('/api/certificates/')
        serializer = CertificateSerializer(instance=self.certificate, context={'request': request})
        data = serializer.data
        self.assertEqual(data['teacher'], str(self.teacher_info.id))
        self.assertEqual(data['file'], request.build_absolute_uri(self.certificate.file.url))

    def test_serializer_file_url(self):
        request = self.factory.get('/api/certificates/')
        serializer = CertificateSerializer(instance=self.certificate, context={'request': request})
        data = serializer.data
        self.assertIn('file', data)
        self.assertTrue(data['file'].startswith('http://testserver'))

    def test_serializer_create(self):
        valid_data = {
            'file': ContentFile(b'file_content', 'certificate.pdf'),
            'teacher': str(self.teacher_info.id)
        }
        serializer = CertificateSerializer(data=valid_data)
        serializer.is_valid(raise_exception=True)
        certificate = serializer.save()
        self.assertEqual(certificate.teacher, self.teacher_info)

    def test_serializer_delete(self):
        serializer = CertificateSerializer(instance=self.certificate)
        self.assertEqual(Certificate.objects.count(), 1)
        serializer.delete(self.certificate)
        self.assertEqual(Certificate.objects.count(), 0)

    def test_serializer_invalid_data(self):
        invalid_data = {
            'file': '',
            'teacher': 'invalid_teacher_id'
        }
        serializer = CertificateSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ArticleSerializerTest(APITestCase):

    def setUp(self):
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article content.',
            image=ContentFile(b'file_content', 'image.jpg'),
            creation_date='2023-07-29'
        )
        self.factory = RequestFactory()

    def test_serializer_valid(self):
        request = self.factory.get('/api/articles/')
        serializer = ArticleSerializer(instance=self.article, context={'request': request})
        data = serializer.data
        self.assertEqual(data['title'], self.article.title)
        self.assertEqual(data['content'], self.article.content)

    def test_serializer_image_url(self):
        request = self.factory.get('/api/articles/')
        self.article.image = ContentFile(b'file_content', 'image.jpg')
        self.article.save()
        serializer = ArticleSerializer(instance=self.article, context={'request': request})
        data = serializer.data
        self.assertIn('image', data)
        self.assertTrue(data['image'].startswith('http://testserver'))


class CourseCategorySerializerTest(APITestCase):

    def setUp(self):
        self.category = CourseCategory.objects.create(name='Test Category')

    def test_serializer_valid(self):
        serializer = CourseCategorySerializer(instance=self.category)
        data = serializer.data
        self.assertEqual(data['name'], self.category.name)


class DiscountSerializerTest(APITestCase):
    def setUp(self):
        self.discount = Discount.objects.create(percent=20, description='Summer Sale')

    def test_serializer_valid(self):
        serializer = DiscountSerializer(instance=self.discount)
        data = serializer.data
        self.assertEqual(data['percent'], self.discount.percent)
        self.assertEqual(data['description'], self.discount.description)


class ReviewSerializerTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='complexpassword',
            first_name='Test',
            last_name='User',
            role='student'
        )
        self.category = CourseCategory.objects.create(name='Test Category')
        self.course = Course.objects.create(
            name='Test Course',
            description='Course description',
            price_for_one=100,
            price_for_many=80,
            course_category=self.category
        )
        self.review = Review.objects.create(
            author='Test Author',
            course=self.course,
            content='Great course!',
            creation_date=timezone.localdate()
        )


    def test_serializer_create(self):
        data = {
            'author': 'New Author',
            'course': self.course.id,
            'content': 'Good course!',
            'creation_date': timezone.localdate().isoformat()
        }
        serializer = ReviewSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        review = serializer.save()
        self.assertIsNotNone(review)
        self.assertEqual(review.author, 'New Author')
        self.assertEqual(review.course.id, self.course.id)
        self.assertEqual(review.content, 'Good course!')
        self.assertEqual(review.creation_date, timezone.localdate())

    def test_serializer_course_data(self):
        serializer = ReviewSerializer(instance=self.review)
        data = serializer.data
        self.assertEqual(data['course']['id'], str(self.course.id))
        self.assertEqual(data['course']['name'], self.course.name)
        self.assertEqual(data['course']['category'], str(self.course.course_category.id))

    def test_serializer_create_invalid(self):
        data = {
            'author': 'New Author',
            'course': self.course.id,
            'creation_date': timezone.localdate().isoformat()
        }
        serializer = ReviewSerializer(data=data)
        self.assertFalse(serializer.is_valid(), msg=serializer.errors)
        self.assertIn('content', serializer.errors)
        data = {
            'author': 'New Author',
            'course': self.course.id,
            'content': 'Good course!',
            'creation_date': 'invalid-date'
        }
        serializer = ReviewSerializer(data=data)
        self.assertFalse(serializer.is_valid(), msg=serializer.errors)
        self.assertIn('creation_date', serializer.errors)


class FaqCategorySerializerTest(APITestCase):
    def setUp(self):
        self.faq_category = FaqCategory.objects.create(name='General')

    def test_serializer_valid(self):
        serializer = FaqCategorySerializer(instance=self.faq_category)
        data = serializer.data
        self.assertEqual(data['name'], self.faq_category.name)


class FaqSerializerTest(APITestCase):
    def setUp(self):
        self.faq_category = FaqCategory.objects.create(name='General')
        self.faq = Faq.objects.create(
            question='What is Django?',
            answer='Django is a high-level Python web framework.',
            faq_category=self.faq_category
        )

    def test_serializer_valid(self):
        serializer = FaqSerializer(instance=self.faq)
        data = serializer.data
        self.assertEqual(data['question'], self.faq.question)
        self.assertEqual(data['answer'], self.faq.answer)


class ApplicationSerializerTest(APITestCase):
    def setUp(self):
        self.course_category = CourseCategory.objects.create(name='Science')
        self.course = Course.objects.create(
            name='Physics',
            description='Physics course',
            study_hours=20,
            price_for_one=100,
            price_for_many=500,
            course_category=self.course_category
        )

    def test_to_representation(self):
        application = Application.objects.create(
            name='John',
            surname='Doe',
            phone_number='+375883475788',
            email='john.doe@example.com',
            start_date=timezone.now().date(),
            course=self.course
        )
        serializer = ApplicationSerializer(instance=application)
        data = serializer.data
        self.assertEqual(data['course']['id'], str(self.course.id))
        self.assertEqual(data['course']['name'], self.course.name)
        self.assertEqual(data['course']['category'], self.course.course_category.id)

    def test_create_valid(self):
        data = {
            'name': 'Jane',
            'surname': 'Doe',
            'phone_number': '+375883475788',
            'email': 'jane.doe@example.com',
            'start_date': timezone.now().date(),
            'course': self.course.id
        }
        serializer = ApplicationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        application = serializer.save()
        self.assertEqual(application.name, 'Jane')
        self.assertEqual(application.surname, 'Doe')
        self.assertEqual(application.phone_number, '+375883475788')

    def test_create_invalid(self):
        data = {
            'name': 'Jane',
            'surname': 'Doe',
            'phone_number': '+375883475788',
            'email': 'jane.doe@example.com',
            'start_date': 'invalid-date',
            'course': self.course.id
        }
        serializer = ApplicationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('start_date', serializer.errors)

    def test_create_invalid_start_date(self):
        data = {
            'name': 'Jane',
            'surname': 'Doe',
            'phone_number': '+375883475788',
            'email': 'jane.doe@example.com',
            'start_date': (timezone.now() - timezone.timedelta(days=1)).date(),
            'course': self.course.id
        }
        serializer = ApplicationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('start_date', serializer.errors)


class CourseSerializerTest(APITestCase):
    def setUp(self):
        self.course_category = CourseCategory.objects.create(name='Science')
        self.teacher_user = User.objects.create(
            username='teacher_user',
            password='pass',
            role='teacher',
            first_name='John',
            last_name='Doe'
        )
        self.teacher_info = TeacherInfo.objects.create(
            user=self.teacher_user,
            education='MSc in Physics',
            experience='5 years of teaching experience'
        )
        self.student_user = User.objects.create(
            username='student_user',
            password='pass',
            role='student',
            first_name='Jane',
            last_name='Doe'
        )
        self.course = Course.objects.create(
            name='Physics',
            description='Physics course',
            study_hours=20,
            price_for_one=100,
            price_for_many=500,
            course_category=self.course_category
        )
        self.course.teachers.add(self.teacher_info)
        self.course.students.add(self.student_user)

    def test_create_invalid(self):
        data = {
            'name': 'Chemistry',
            'description': 'Chemistry course',
            'study_hours': 'invalid-study-hours',
            'price_for_one': 150,
            'price_for_many': 600,
            'course_category': self.course_category.id
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('study_hours', serializer.errors)

    def test_to_representation(self):
        serializer = CourseSerializer(instance=self.course)
        data = serializer.data
        self.assertEqual(data['name'], self.course.name)
        self.assertEqual(data['description'], self.course.description)
        self.assertEqual(uuid.UUID(data['course_category']['id']), self.course_category.id)
        self.assertEqual(data['course_category']['name'], self.course_category.name)
        teacher_ids = [teacher['id'] for teacher in data['teachers']]
        self.assertIn(str(self.teacher_info.id), teacher_ids)
        student_ids = [student['id'] for student in data['students']]
        self.assertIn(str(self.student_user.id), student_ids)

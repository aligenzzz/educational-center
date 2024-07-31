import uuid

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api_product.models import TeacherInfo, Certificate, Article, CourseCategory, Course, Discount, Review, FaqCategory, \
    Faq, Application
from api_product.serializers import TeacherInfoSerializer, CertificateSerializer, ArticleSerializer, \
    CourseCategorySerializer, CourseSerializer, DiscountSerializer, ReviewSerializer, FaqCategorySerializer, \
    FaqSerializer, ApplicationSerializer
from django.urls import reverse
from api_authentication.models import User


class TeacherInfoViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            password='password',
            first_name='Test',
            last_name='User',
            role='teacher'
        )
        self.teacher = TeacherInfo.objects.create(user=self.user, education='PhD', experience='10 years')

    def test_list_teacherinfo(self):
        response = self.client.get(reverse('teacher-info-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_teacherinfo(self):
        response = self.client.get(reverse('teacher-info-detail', args=[self.teacher.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['education'], self.teacher.education)

    def test_update_teacherinfo(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(reverse('teacher-info-detail', args=[self.teacher.id]), {
            'education': 'Master',
            'experience': '12 years'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.education, 'Master')

    def test_partial_update_teacherinfo(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('teacher-info-detail', args=[self.teacher.id]), {'experience': '15 years'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.experience, '15 years')

    def test_update_teacherinfo_unauthenticated(self):
        response = self.client.put(reverse('teacher-info-detail', args=[self.teacher.id]), {
            'education': 'Master',
            'experience': '12 years'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CertificateViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            password='password',
            first_name='Test',
            last_name='User',
            role='teacher'
        )
        self.teacher = TeacherInfo.objects.create(user=self.user, education='PhD', experience='10 years')
        self.certificate_file = SimpleUploadedFile(
            name="test_certificate.pdf",
            content=b"file_content",
            content_type="application/pdf"
        )
        self.certificate = Certificate.objects.create(
            teacher=self.teacher,
            file=self.certificate_file
        )

    def test_list_certificates(self):
        response = self.client.get(reverse('certificates-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_certificate(self):
        response = self.client.get(reverse('certificates-detail', args=[self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher'], str(self.teacher.id))

    def test_create_certificate_with_file(self):
        self.client.force_authenticate(user=self.user)
        new_certificate_file = SimpleUploadedFile(
            name="new_certificate.pdf",
            content=b"new file content",
            content_type="application/pdf"
        )
        response = self.client.post(reverse('certificates-list'), {
            'teacher': self.teacher.id,
            'file': new_certificate_file
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('file', response.data)

    def test_create_certificate_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('certificates-list'), {
            'teacher': '',
            'file': ''
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_certificate(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('certificates-detail', args=[self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_certificate_unauthenticated(self):
        response = self.client.delete(reverse('certificates-detail', args=[self.certificate.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ArticleViewSetTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.article1 = Article.objects.create(
            title="Test Article 1",
            content="This is the content of test article 1",
            creation_date=timezone.localdate(),
            source="Source 1"
        )
        self.article2 = Article.objects.create(
            title="Test Article 2",
            content="This is the content of test article 2",
            creation_date='2023-07-30',
            source="Source 2"
        )

    def test_list_articles(self):
        response = self.client.get(reverse('articles-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.article1.title)
        self.assertEqual(response.data[1]['title'], self.article2.title)

    def test_retrieve_article(self):
        response = self.client.get(reverse('articles-detail', args=[self.article1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.article1.title)
        self.assertEqual(response.data['content'], self.article1.content)

    def test_retrieve_article_not_found(self):
        non_existent_id = uuid.uuid4()
        response = self.client.get(reverse('articles-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CourseCategoryViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category1 = CourseCategory.objects.create(name="Category 1")
        self.category2 = CourseCategory.objects.create(name="Category 2")

    def test_list_course_categories(self):
        response = self.client.get(reverse('course-categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.category2.name)
        self.assertEqual(response.data[1]['name'], self.category1.name)

    def test_retrieve_course_category(self):
        response = self.client.get(reverse('course-categories-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category1.name)

    def test_retrieve_non_existent_course_category(self):
        non_existent_id = uuid.uuid4()
        response = self.client.get(reverse('course-categories-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DiscountViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.discount1 = Discount.objects.create(percent=10, description="10% off")
        self.discount2 = Discount.objects.create(percent=20, description="20% off")

    def test_list_discounts(self):
        response = self.client.get(reverse('discounts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['percent'], self.discount2.percent)
        self.assertEqual(response.data[1]['percent'], self.discount1.percent)

    def test_retrieve_discount(self):
        response = self.client.get(reverse('discounts-detail', args=[self.discount1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['percent'], self.discount1.percent)
        self.assertEqual(response.data['description'], self.discount1.description)

    def test_retrieve_non_existent_discount(self):
        non_existent_id = uuid.uuid4()
        response = self.client.get(reverse('discounts-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CourseCategory.objects.create(name='Test Category')
        self.course = Course.objects.create(
            name='Test Course',
            description='Course description',
            price_for_one=100,
            price_for_many=80,
            course_category=self.category
        )
        self.review1 = Review.objects.create(
            author="Author 1",
            course=self.course,
            content="Review content 1",
            creation_date=timezone.now()
        )
        self.review2 = Review.objects.create(
            author="Author 2",
            course=self.course,
            content="Review content 2",
            creation_date=timezone.now()
        )

    def test_list_reviews(self):
        response = self.client.get(reverse('reviews-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(parse_date(response.data[0]['creation_date']), self.review2.creation_date.date())
        self.assertEqual(parse_date(response.data[1]['creation_date']), self.review1.creation_date.date())

    def test_retrieve_review(self):
        response = self.client.get(reverse('reviews-detail', args=[self.review1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['author'], self.review1.author)
        self.assertEqual(response.data['content'], self.review1.content)

    def test_retrieve_non_existent_review(self):
        non_existent_id = uuid.uuid4()
        response = self.client.get(reverse('reviews-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_review(self):
        data = {
            'author': 'New Author',
            'course': self.course.id,
            'content': 'New review content',
            'creation_date': timezone.now().date()
        }
        response = self.client.post(reverse('reviews-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], data['author'])
        self.assertEqual(response.data['content'], data['content'])

    def test_create_review_invalid_data(self):
        data = {
            'author': '',
            'course': self.course.id,
            'content': '',
            'creation_date': timezone.now().date()
        }
        response = self.client.post(reverse('reviews-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FaqCategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category1 = FaqCategory.objects.create(name='General')
        self.category2 = FaqCategory.objects.create(name='Technical')

    def test_list_faq_categories(self):
        response = self.client.get(reverse('faq-categories-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Technical')
        self.assertEqual(response.data[1]['name'], 'General')

    def test_retrieve_faq_category(self):
        response = self.client.get(reverse('faq-categories-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category1.name)

    def test_retrieve_faq_category_not_found(self):
        response = self.client.get(reverse('faq-categories-detail', args=['nonexistent-uuid']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FaqViewSetTest(APITestCase):
    def setUp(self):
        self.category = FaqCategory.objects.create(name='General')
        self.faq1 = Faq.objects.create(question='How to reset password?', answer='Follow these steps...',
                                       faq_category=self.category)
        self.faq2 = Faq.objects.create(question='Where to find the user manual?',
                                       answer='It is located in the help section...', faq_category=self.category)

    def test_list_faqs(self):
        response = self.client.get(reverse('faqs-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['question'], self.faq1.question)
        self.assertEqual(response.data[1]['question'], self.faq2.question)

    def test_retrieve_faq(self):
        response = self.client.get(reverse('faqs-detail', args=[self.faq1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], self.faq1.question)
        self.assertEqual(response.data['answer'], self.faq1.answer)
        self.assertEqual(response.data['faq_category']['id'], str(self.faq1.faq_category.id))
        self.assertEqual(response.data['faq_category']['name'], self.faq1.faq_category.name)

    def test_retrieve_faq_not_found(self):
        response = self.client.get(reverse('faqs-detail', args=['nonexistent-uuid']))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ApplicationViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='user',
            password='password',
            first_name='Test',
            last_name='User',
            role='teacher'
        )
        self.course_category = CourseCategory.objects.create(
            name='General'
        )
        self.course = Course.objects.create(
            name='Sample Course',
            price_for_one=100,
            price_for_many=200,
            study_hours=10,
            course_category=self.course_category
        )
        self.application1 = Application.objects.create(
            name='John',
            surname='Doe',
            phone_number='+375445768788',
            email='john.doe@example.com',
            start_date=timezone.now().date(),
            course=self.course
        )
        self.application2 = Application.objects.create(
            name='Jane',
            surname='Smith',
            phone_number='+375445768788',
            email='jane.smith@example.com',
            start_date=timezone.now().date(),
            course=self.course
        )

    def test_list_applications(self):
        response = self.client.get(reverse('applications-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.application1.name)
        self.assertEqual(response.data[1]['name'], self.application2.name)

    def test_retrieve_application(self):
        response = self.client.get(reverse('applications-detail', args=[self.application1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.application1.name)
        self.assertEqual(response.data['surname'], self.application1.surname)
        self.assertEqual(response.data['phone_number'], self.application1.phone_number)
        self.assertEqual(response.data['email'], self.application1.email)
        self.assertEqual(response.data['start_date'], str(self.application1.start_date))
        self.assertEqual(response.data['course']['id'], str(self.course.id))

    def test_create_application(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New',
            'surname': 'Applicant',
            'phone_number': '+375445768788',
            'email': 'new.applicant@example.com',
            'start_date': timezone.now().date(),
            'course': str(self.course.id)
        }
        response = self.client.post(reverse('applications-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New')
        self.assertEqual(response.data['surname'], 'Applicant')
        self.assertEqual(response.data['phone_number'], '+375445768788')
        self.assertEqual(response.data['email'], 'new.applicant@example.com')
        self.assertEqual(response.data['course']['id'], str(self.course.id))

    def test_create_application_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': '',
            'surname': '',
            'phone_number': 'invalidphone',
            'email': 'invalidemail',
            'start_date': '2023-01-01',
            'course': str(self.course.id)
        }
        response = self.client.post(reverse('applications-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CourseViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = CourseCategory.objects.create(name='Programming')
        self.teacher = TeacherInfo.objects.create(
            user=User.objects.create_user(
                username='teacher',
                password='password',
                first_name='John',
                last_name='Doe',
                role='teacher'
            ),
            education='PhD in Computer Science',
            experience='10 years in teaching'
        )
        self.course = Course.objects.create(
            name='Python 101',
            description='Introduction to Python',
            study_hours=30,
            price_for_one=150,
            price_for_many=1200,
            course_category=self.category
        )

    def test_list_courses(self):
        response = self.client.get(reverse('courses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.course.name)
        self.assertEqual(response.data[0]['course_category']['name'], self.category.name)

    def test_retrieve_course(self):
        response = self.client.get(reverse('courses-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.course.name)
        self.assertEqual(response.data['course_category']['name'], self.category.name)

    def test_course_not_found(self):
        invalid_id = '12345678-1234-5678-1234-567812345678'
        response = self.client.get(reverse('courses-detail', args=[invalid_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

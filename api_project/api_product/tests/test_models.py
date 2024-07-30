from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.test import TestCase
from api_product.models import TeacherInfo, Certificate, Article, CourseCategory, Discount, Course, Review, FaqCategory, \
    Faq, Application
from api_authentication.models import User
from django.utils import timezone
from api_product.forms import CourseForm


class TeacherInfoModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='teacheruser',
            password='complexpassword',
            first_name='Teacher',
            last_name='User',
            role='teacher'
        )
        self.teacher_info = TeacherInfo.objects.create(
            user=self.user,
            education='PhD in Computer Science',
            experience='10 years of experience'
        )

    def test_teacher_info_creation(self):
        self.assertTrue(isinstance(self.teacher_info, TeacherInfo))
        self.assertEqual(str(self.teacher_info), self.user.last_name + " " + self.user.first_name)

    def test_teacher_info_fields(self):
        self.assertEqual(self.teacher_info.user, self.user)
        self.assertEqual(self.teacher_info.education, 'PhD in Computer Science')
        self.assertEqual(self.teacher_info.experience, '10 years of experience')

    def test_full_name_property(self):
        self.assertEqual(self.teacher_info.full_name, self.user.last_name + " " + self.user.first_name)

    def test_blank_photo(self):
        self.assertIsNone(self.teacher_info.photo.name if self.teacher_info.photo else None)


class CertificateModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='teacheruser',
            password='complexpassword',
            first_name='Teacher',
            last_name='User',
            role='teacher'
        )
        self.teacher_info = TeacherInfo.objects.create(
            user=self.user,
            education='PhD in Computer Science',
            experience='10 years of experience'
        )
        self.certificate_file = ContentFile("Test Certificate Content", "test_cert.pdf")
        self.certificate = Certificate.objects.create(
            file=self.certificate_file,
            teacher=self.teacher_info
        )

    def test_certificate_creation(self):
        self.assertTrue(isinstance(self.certificate, Certificate))
        self.assertEqual(str(self.certificate), f'Certificate ({self.teacher_info})')

    def test_certificate_fields(self):
        self.assertTrue(self.certificate.file.name.startswith('certificates/test_cert'))
        self.assertEqual(self.certificate.teacher, self.teacher_info)

    def test_blank_file(self):

        certificate = Certificate.objects.create(
            file=None,
            teacher=self.teacher_info
        )
        self.assertIsNone(certificate.file.name if certificate.file else None)


class ArticleModelTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article content.',
            creation_date=timezone.localdate(),
        )

    def test_article_creation(self):
        self.assertTrue(isinstance(self.article, Article))
        self.assertEqual(str(self.article), 'Test Article')

    def test_article_fields(self):
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.content, 'This is a test article content.')
        self.assertEqual(self.article.creation_date, timezone.localdate())

    def test_blank_image(self):
        self.assertIsNone(self.article.image.name if self.article.image else None)


class CourseCategoryModelTest(TestCase):
    def setUp(self):
        self.category = CourseCategory.objects.create(name='Test Category')

    def test_course_category_creation(self):
        self.assertTrue(isinstance(self.category, CourseCategory))
        self.assertEqual(str(self.category), 'Test Category')

    def test_unique_name(self):
        with self.assertRaises(Exception):
            CourseCategory.objects.create(name='Test Category')


class DiscountModelTest(TestCase):

    def setUp(self):
        self.discount = Discount.objects.create(percent=15, description='Test Discount')

    def test_discount_creation(self):
        self.assertTrue(isinstance(self.discount, Discount))
        self.assertEqual(str(self.discount), '15 %')

    def test_discount_fields(self):
        self.assertEqual(self.discount.percent, 15)
        self.assertEqual(self.discount.description, 'Test Discount')

    def test_percent_validator(self):
        with self.assertRaises(ValidationError):
            discount = Discount(percent=100, description='Invalid Discount')
            discount.full_clean()


class ReviewModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Course Description',
            study_hours=40,
            price_for_one=1000,
            price_for_many=2000,
            course_category=CourseCategory.objects.create(name='Test Category')
        )
        self.review = Review.objects.create(
            author='Test Author',
            course=self.course,
            content='This is a test review content.',
            creation_date=timezone.localdate()
        )

    def test_review_creation(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(str(self.review), f'Review by {self.review.author} on {self.course.name}')

    def test_review_fields(self):
        self.assertEqual(self.review.author, self.review.author)
        self.assertEqual(self.review.content, self.review.content)
        self.assertEqual(self.review.creation_date, timezone.localdate())
        self.assertEqual(self.review.course, self.course)


class FaqCategoryModelTest(TestCase):
    def setUp(self):
        self.faq_category = FaqCategory.objects.create(name='Test Faq Category')

    def test_faq_category_creation(self):
        self.assertTrue(isinstance(self.faq_category, FaqCategory))
        self.assertEqual(str(self.faq_category), self.faq_category.name)

    def test_unique_name(self):
        with self.assertRaises(Exception):
            FaqCategory.objects.create(name='Test Faq Category')


class FaqModelTest(TestCase):

    def setUp(self):
        self.faq_category = FaqCategory.objects.create(name='Test Faq Category')
        self.faq = Faq.objects.create(
            question='What is Django?',
            answer='Django is a high-level Python web framework.',
            faq_category=self.faq_category
        )

    def test_faq_creation(self):
        self.assertTrue(isinstance(self.faq, Faq))
        self.assertEqual(str(self.faq), self.faq.question)

    def test_faq_fields(self):
        self.assertEqual(self.faq.question, 'What is Django?')
        self.assertEqual(self.faq.answer, 'Django is a high-level Python web framework.')
        self.assertEqual(self.faq.faq_category, self.faq_category)


class ApplicationModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Course Description',
            study_hours=40,
            price_for_one=1000,
            price_for_many=2000,
            course_category=CourseCategory.objects.create(name='Test Category')
        )
        self.application = Application.objects.create(
            name='John',
            surname='Doe',
            phone_number='+375338685844',
            email='john.doe@example.com',
            start_date=timezone.localdate(),
            course=self.course
        )

    def test_application_creation(self):
        self.assertTrue(isinstance(self.application, Application))
        self.assertEqual(str(self.application), 'John Doe — Test Course')

    def test_application_fields(self):
        self.assertEqual(self.application.name, 'John')
        self.assertEqual(self.application.surname, 'Doe')
        self.assertEqual(self.application.phone_number, '+375338685844')
        self.assertEqual(self.application.email, 'john.doe@example.com')
        self.assertEqual(self.application.start_date, timezone.localdate())
        self.assertEqual(self.application.course, self.course)

    def test_save_method(self):
        application = Application.objects.create(
            name='Jane',
            surname='Doe',
            phone_number='+375338685844',
            email='jane.doe@example.com',
            course=self.course
        )
        self.assertEqual(application.start_date, timezone.now().date())

    def test_clean_method(self):
        with self.assertRaises(ValidationError):
            application = Application(
                name='Future Applicant',
                surname='Doe',
                phone_number='+375338685844',
                email='future.applicant@example.com',
                start_date=timezone.now().date() - timezone.timedelta(days=1),
                course=self.course
            )
            application.clean()


class CourseModelTest(TestCase):
    def setUp(self):
        self.category = CourseCategory.objects.create(name='Test Category')
        self.teacher = TeacherInfo.objects.create(
            user=User.objects.create_user(
                username='teacheruser',
                password='complexpassword',
                first_name='Teacher',
                last_name='User',
                role='teacher'
            ),
            education='PhD in Computer Science',
            experience='10 years of experience'
        )
        self.student = User.objects.create_user(
            username='studentuser',
            password='complexpassword',
            first_name='Student',
            last_name='User',
            role='student'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Course Description',
            study_hours=40,
            price_for_one=1000,
            price_for_many=2000,
            course_category=self.category
        )
        self.course.teachers.add(self.teacher)
        self.course.students.add(self.student)

    def test_course_creation(self):
        self.assertTrue(isinstance(self.course, Course))
        self.assertEqual(str(self.course), 'Test Course')

    def test_course_fields(self):
        self.assertEqual(self.course.name, 'Test Course')
        self.assertEqual(self.course.description, 'Test Course Description')
        self.assertEqual(self.course.study_hours, 40)
        self.assertEqual(self.course.price_for_one, 1000)
        self.assertEqual(self.course.price_for_many, 2000)
        self.assertEqual(self.course.course_category, self.category)

    def test_course_teachers_and_students(self):
        self.assertIn(self.teacher, self.course.teachers.all())
        self.assertIn(self.student, self.course.students.all())

    def test_clean_method_valid(self):
        valid_student = User.objects.create_user(
            username='validstudent',
            password='complexpassword',
            first_name='Valid',
            last_name='Student',
            role='student'
        )
        self.course.students.add(valid_student)
        try:
            self.course.clean()
        except ValidationError:
            self.fail('clean() raised ValidationError unexpectedly for a valid student.')

    def test_form_invalid_student(self):
        invalid_student = User.objects.create_user(
            username='invaliduser',
            password='complexpassword',
            first_name='Invalid',
            last_name='User',
            role='invalid'
        )
        form_data = {
            'name': 'Test Course',
            'description': 'Test Description',
            'study_hours': 10,
            'price_for_one': 100,
            'price_for_many': 200,
            'course_category': self.category.id,
            'students': [invalid_student.id],
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('students', form.errors)

    def test_form_valid_student(self):
        valid_student = User.objects.create_user(
            username='validuser',
            password='complexpassword',
            first_name='Valid',
            last_name='User',
            role='student'
        )
        form_data = {
            'name': 'Test Course',
            'description': 'Test Description',
            'study_hours': 10,
            'price_for_one': 100,
            'price_for_many': 200,
            'course_category': self.category.id,
            'students': [valid_student.id],
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())

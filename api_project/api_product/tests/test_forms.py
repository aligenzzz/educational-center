from django.test import TestCase
from api_authentication.models import User
from ..forms import TeacherInfoForm, CourseForm
from ..models import TeacherInfo, CourseCategory, Course


class CourseFormTest(TestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='teacheruser',
            password='complexpassword',
            first_name='Teacher',
            last_name='User',
            role='teacher'
        )
        self.student_user = User.objects.create_user(
            username='studentuser',
            password='complexpassword',
            first_name='Student',
            last_name='User',
            role='student'
        )
        self.course_category = CourseCategory.objects.create(
            name='Science'
        )
        self.teacher_info = TeacherInfo.objects.create(
            user=self.teacher_user,
            education='PhD in Physics',
            experience='15 years'
        )

    def test_valid_form(self):
        form_data = {
            'name': 'Physics 101',
            'description': 'An introductory course to Physics.',
            'image': None,  # Assuming we do not test file uploads here
            'advantages': 'Comprehensive curriculum',
            'curriculum': 'Basic physics concepts',
            'study_hours': 40,
            'price_for_one': 100,
            'price_for_many': 80,
            'teachers': [self.teacher_info.id],
            'students': [self.student_user.id],
            'course_category': self.course_category.id
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'name': '',  # Invalid as name is required
            'description': '',
            'image': None,
            'advantages': '',
            'curriculum': '',
            'study_hours': None,  # Invalid as study_hours is required
            'price_for_one': None,  # Invalid as price_for_one is required
            'price_for_many': None,  # Invalid as price_for_many is required
            'teachers': [],
            'students': [],
            'course_category': None  # Invalid as course_category is required
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('study_hours', form.errors)
        self.assertIn('price_for_one', form.errors)
        self.assertIn('price_for_many', form.errors)
        self.assertIn('course_category', form.errors)


class TeacherInfoFormTest(TestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='teacheruser',
            password='complexpassword',
            first_name='Teacher',
            last_name='User',
            role='teacher'
        )
        self.student_user = User.objects.create_user(
            username='studentuser',
            password='complexpassword',
            first_name='Student',
            last_name='User',
            role='student'
        )

    def test_valid_form(self):
        form_data = {
            'user': self.teacher_user.id,
            'photo': None,
            'education': 'PhD in Education',
            'experience': '10 years of teaching experience'
        }
        form = TeacherInfoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_role(self):
        form_data = {
            'user': self.student_user.id,
            'photo': None,
            'education': 'Some education',
            'experience': 'Some experience'
        }
        form = TeacherInfoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user', form.errors)

    def test_invalid_form_missing_fields(self):
        form_data = {
            'user': self.teacher_user.id,
            'photo': None,
            'education': '',
            'experience': ''
        }
        form = TeacherInfoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('education', form.errors)
        self.assertIn('experience', form.errors)

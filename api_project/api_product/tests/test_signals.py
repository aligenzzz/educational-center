import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from ..models import Course, CourseCategory, Certificate, TeacherInfo
from api_authentication.models import User


class CourseSignalsTest(TestCase):
    def setUp(self):
        self.category = CourseCategory.objects.create(name='Test Category')
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
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            price_for_one=1000,
            price_for_many=2000,
            study_hours=30,
            course_category_id=self.category.id
        )

    def test_valid_student_addition(self):
        self.course.students.add(self.student_user)
        self.assertIn(self.student_user, self.course.students.all())

    def test_invalid_student_addition(self):
        with self.assertRaises(ValidationError):
            self.course.students.add(self.teacher_user)
            m2m_changed.send(
                sender=self.course.students.through,
                instance=self.course,
                action='pre_add',
                pk_set={self.teacher_user.pk}
            )

    def test_valid_student_addition_with_signal(self):
        m2m_changed.send(
            sender=self.course.students.through,
            instance=self.course,
            action='pre_add',
            pk_set={self.student_user.pk}
        )
        self.course.students.add(self.student_user)
        self.assertIn(self.student_user, self.course.students.all())


class CertificateSignalsTest(TestCase):
    def setUp(self):
        self.teacher = TeacherInfo.objects.create(
            user=User.objects.create_user(
                username='teacheruser',
                password='complexpassword',
                first_name='Teacher',
                last_name='User',
                role='teacher'
            ),
            education='PhD',
            experience='10 years'
        )
        self.certificate_file = ContentFile("Test Certificate Content", "test_cert.pdf")
        self.certificate = Certificate.objects.create(
            file=self.certificate_file,
            teacher=self.teacher
        )

    def test_file_deletion_on_certificate_delete(self):
        file_name = self.certificate.file.name
        self.certificate.delete()
        self.assertFalse(default_storage.exists(file_name))

    def test_file_exists_before_deletion(self):
        file_name = self.certificate.file.name
        self.assertTrue(default_storage.exists(file_name))

    def test_file_not_deleted_if_no_file(self):
        certificate_no_file = Certificate.objects.create(
            file=None,
            teacher=self.teacher
        )
        self.assertIsNone(certificate_no_file.file.name if certificate_no_file.file else None)
        certificate_no_file.delete()
        self.assertIsNone(certificate_no_file.file.name if certificate_no_file.file else None)

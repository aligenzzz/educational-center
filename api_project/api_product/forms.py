from django import forms
from api_authentication.models import User
from django.core.exceptions import ValidationError

from .models import TeacherInfo, Course


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(role='teacher')

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if user and user.role != 'teacher':
            raise ValidationError(f'User {user.username} does not have the role "teacher"')
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = User.objects.filter(role='student')


        
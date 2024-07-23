from django import forms
from api_authentication.models import User
from .models import TeacherInfo, Course


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(role='teacher')
        

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = User.objects.filter(role='student')
        
from api_authentication.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronymic', 
                  'email', 'phone_number', 'role', 'password1', 'password2')


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'patronymic', 
                  'email', 'phone_number', 'role')
        
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+375\d{9}$',
    message='Phone number must be entered in the format: +375XXXXXXXXX.',
)

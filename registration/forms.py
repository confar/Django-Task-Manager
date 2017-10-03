from django.forms import Form, CharField, EmailField
from django.forms.utils import ErrorList


class RegistrationForm(Form):
    username = CharField(required=True)
    email = EmailField(required=True)
    password = CharField(required=True)
    confirm_password = CharField(required=True)
    first_name = CharField(required=False)
    last_name = CharField(required=False)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self._errors['password'] = ErrorList('The passwords you entered do not match')

        return cleaned_data

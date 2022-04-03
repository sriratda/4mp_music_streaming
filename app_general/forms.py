from django import forms
from .models import UserTest

class UserModelForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=UserTest
        fields=['email', 'name','password']

    def clean(self):
        cleaned_data = super(UserModelForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    # class Meta:
    #     model = User
    #     fields = ['email', 'name', 'password']
    #     labels = {
    #         'email': 'E-mail',
    #         'name': 'Username',
    #         'password': 'Password'
    #     }

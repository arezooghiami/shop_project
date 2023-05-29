from django import forms
from django.contrib.auth.models import User
from .models import *

error = {
    'required': 'لطفا مقدار وارد نمایید',
    'min_length' : 'حداحق می بایست 5 کاراکتر باشد',
    'invalid' : 'عبارت وارد شده صحیح نمی باشد',
}




class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'UserName'}))
    email = forms.EmailField(error_messages=error)
    first_name = forms.CharField(max_length=100,min_length=5,error_messages=error)
    last_name = forms.CharField(max_length=100)
    password_1 = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'palceholder':'پسورد خود را و.ارد نمایید'}))
    password_2 = forms.CharField(max_length=20)

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('User Exists')
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ایمیل تکراری است')
        return email

    def clean_password_2(self):
        password1 = self.cleaned_data['password_1']
        password2 = self.cleaned_data['password_2']
        if password1 != password2:
            raise forms.ValidationError('password is wrong')
        elif len(password2) < 8 :
            raise forms.ValidationError('Password is short')
        elif not any(x.isupper() for x in password2):
            raise forms.ValidationError('حداقل یک کاراکتر بزرگ داشته باشد')
        return password2

class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['phone','address','profile_image']







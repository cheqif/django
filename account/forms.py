from django import forms
from django.contrib import auth #引入auth模块
from django.contrib.auth.models import User # auth应用中引入User类
from django.core.exceptions import ValidationError
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名")
    #下面有一个全角的空格
    password = forms.CharField(widget=forms.PasswordInput,label="密　码")


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password', 'password2')

    def clean_username(self):
        cu = User.objects.filter(username=self.cleaned_data['username']).values('id')
        if cu:
            raise ValidationError('用户已存在')
        return self.cleaned_data['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次输入的密码不一致')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
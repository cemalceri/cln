# from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     password_confirm = forms.CharField(widget=forms.PasswordInput())
#     field_order = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm']
#
#     class Meta:
#         model = User
#         fields = {'first_name', 'last_name', 'username', 'email', 'password', 'password_confirm'}
#
#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#         # for field in self.fields:
#         #     self.fields[field].widget.attrs = {'class': 'form-control'}
#         self.fields['first_name'].widget.attrs = {'class': 'form-control form-control-user',
#                                                   'placeholder': 'İsim', 'required': 'true'}
#         self.fields['last_name'].widget.attrs = {'class': 'form-control form-control-user', 'placeholder': 'Soy İsim',
#                                                  'required': 'true'}
#         self.fields['username'].widget.attrs = {'class': 'form-control form-control-user',
#                                                 'placeholder': 'Kullanıcı Adı'}
#         self.fields['email'].widget.attrs = {'class': 'form-control form-control-user', 'placeholder': 'E-Mail',
#                                              'required': 'true'}
#         self.fields['password'].widget.attrs = {'class': 'form-control form-control-user', 'placeholder': 'Şifre'}
#         self.fields['password_confirm'].widget.attrs = {'class': 'form-control form-control-user',
#                                                         'placeholder': 'Tekrar Şifre'}
#
#     def clean(self):
#         password = self.cleaned_data.get('password')
#         password_confirm = self.cleaned_data.get('password_confirm')
#         if password != password_confirm:
#             self.add_error('password', 'Şifreler eşleşmiyor!')
#
#         username = self.cleaned_data.get('username')
#         username = username.lower()
#         if User.objects.filter(username=username).exists():
#             self.add_error('username', 'Bu kullanıcı adı zaten kullanılıyor!')
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         email = email.lower()
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('Bu mail adresi zaten kullanılıyor!!')
#         return email


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı',
                                          'icon': 'fa-user-check'}))
    password = forms.CharField(required=True, max_length=50,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Şifre',
                                          'icon': 'fa-lock'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     if not user:
    #         self.add_error('password', 'Kullanıcı adı veya şifre geçersiz!')
    #         # raise forms.ValidationError('User name or password is not valid!')

    def clean_username(self):
        data = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", data):
            user = User.objects.filter(email__iexact=data)
            if len(user) == 1:
                return user.first().username
        return data

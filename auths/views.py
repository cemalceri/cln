from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .decorators import anonymous_required
from .forms import  LoginForm


def index(request):
    return HttpResponseRedirect(reverse('dashboard'))

#
# @anonymous_required
# def user_register(request):
#     form = RegisterForm(data=request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         password = form.cleaned_data.get('password')
#         user.set_password(password)
#         user.is_active = False
#         user.save()
#         messages.success(request, 'Kullanıcı kayıt edildi. Yönetici onayladıktan sonra giriş yapabilirsiniz.')
#         return HttpResponseRedirect(reverse('home'))
#     return render(request, 'auth/register.html', context={'form': form})


@anonymous_required
def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.filter(username=username).first()
        if user:
            if user.is_active:
                is_user_auth = authenticate(username=username, password=password)
                if is_user_auth:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    msg = 'Hoşgeldin  %s!' % user.first_name
                    messages.success(request, msg)
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    messages.error(request, "Geçersiz kullanıcı adı veya şifre")
            else:
                messages.error(request, "Hesabınız yönetici tarafından henüz onaylanmamış.")
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre")
    return render(request, 'auth/signin.html', context={'form': form})


def user_logout(request):
    msg = 'Hoşça Kal! %s' % request.user.username
    logout(request)
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('login'))

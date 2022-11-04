from django.urls import path, include

from auths import views

urlpatterns = [
    # path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    # path('profile/', views.user_profile, name='user_profile'),
    # path('profile/<username>', views.user_profile, name='user_profile'),
    # path('recover-pasword', views.user_register, name='recover_password'),
    # path('social/', include('social_django.urls'), name='social'),
    # path(r'captcha/', include('captcha.urls')),
]

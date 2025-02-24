from django.urls import path
from . import views

app_name = 'edu'

urlpatterns = [
    path('student/', views.signup_view, name = "student_dashboard"),
    path('teacher/', views.login_view, name = "teacher_dashboard"),
    path('logout/', views.logout_view, name = "logout"),
]

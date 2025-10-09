
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:slug>/buy/', views.initiate_payment, name='initiate_payment'),
    path('paystack/verify/', views.verify_payment, name='verify_payment'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('exam/<int:course_id>/', views.take_exam, name='take_exam'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-course/', views.add_course, name='add_course'),
    path('admin/<slug:course_slug>/add-module/', views.add_module, name='add_module'),
    path('', views.index, name='index'),
    path('about/', views.about_page, name='about'),
]


from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Enrollment, ReferralCode, Exam, Question, Submission, Certificate, Payment
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, CourseForm, ModuleForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.conf import settings
from django.http import HttpResponse
import requests

def index(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/index.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(user=request.user, course=course, purchased=True).exists()
    return render(request, 'courses/course_detail.html', {'course': course, 'enrolled': enrolled, 'whatsapp': '+2348050783205S'})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('courses:index')
    else:
        form = SignUpForm()
    return render(request, 'courses/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('courses:index')
    else:
        form = AuthenticationForm()
        return render(request, 'courses/login.html', {'form': form})
    return render(request, 'courses/login.html', {'form': form})

@login_required
def initiate_payment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    user = request.user
    payment = Payment.objects.create(user=user, course=course, amount=int(course.price), ref='')
    payment.save()
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    data = {
        "email": user.email,
        "amount": int(course.price * 100),
        "reference": payment.ref,
        "callback_url": request.build_absolute_uri('/paystack/verify/')
    }
    r = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)
    res = r.json()
    if res.get('status'):
        return redirect(res['data']['authorization_url'])
    return HttpResponse('Error initiating payment.')

def verify_payment(request):
    ref = request.GET.get('reference') or request.GET.get('trxref') or request.GET.get('reference')
    if not ref:
        return HttpResponse('No reference provided.')
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    r = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    res = r.json()
    try:
        payment = Payment.objects.get(ref=ref)
    except Payment.DoesNotExist:
        return HttpResponse('Payment record not found.')
    if res.get('data') and res['data'].get('status') == 'success':
        payment.verified = True
        payment.save()
        enrollment, _ = Enrollment.objects.get_or_create(user=payment.user, course=payment.course)
        enrollment.mark_purchased()
        return render(request, 'courses/payment_success.html', {'payment': payment})
    return render(request, 'courses/payment_failed.html', {'payment': payment, 'res': res})

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user, purchased=True)
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})

@login_required
def take_exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    exam = Exam.objects.filter(course=course).first()
    if not exam:
        return HttpResponse('No exam for this course yet.')
    questions = exam.questions.all()
    if request.method == 'POST':
        total = questions.count()
        correct = 0
        for q in questions:
            ans = request.POST.get(str(q.id),'').upper()
            if ans == q.correct:
                correct += 1
        score = int((correct/total)*100) if total>0 else 0
        passed = score >= exam.passing_score
        Submission.objects.create(exam=exam, user=request.user, score=score, passed=passed)
        if passed:
            Certificate.objects.create(user=request.user, course=course)
        return render(request, 'courses/exam_result.html', {'score': score, 'passed': passed})
    return render(request, 'courses/take_exam.html', {'exam': exam, 'questions': questions})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    users = __import__('django.contrib.auth').contrib.auth.get_user_model().objects.all()
    total_courses = Course.objects.count()
    enrolls = Enrollment.objects.exclude(used_referral=None).values('used_referral').annotate(count=Count('id'))
    return render(request, 'adminpanel/dashboard.html', {'users': users, 'total_courses': total_courses, 'enrolls': enrolls})

@user_passes_test(lambda u: u.is_superuser)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:index')
    else:
        form = CourseForm()
    return render(request, 'adminpanel/add_course.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def add_module(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            mod = form.save(commit=False)
            mod.course = course
            mod.save()
            return redirect('courses:course_detail', slug=course.slug)
    else:
        form = ModuleForm()
    return render(request, 'adminpanel/add_module.html', {'form': form, 'course': course})

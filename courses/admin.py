
from django.contrib import admin
from .models import Course, Module, Enrollment, ReferralCode, Exam, Question, Submission, Certificate, Payment
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(ReferralCode)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Certificate)
admin.site.register(Payment)

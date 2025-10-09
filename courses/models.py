
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

class ReferralCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self): return self.code

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    def __str__(self): return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    video_url = models.URLField(blank=True)
    note = models.TextField(blank=True, null=True)
    class Meta:
        ordering = ['order']
    def __str__(self): return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(null=True, blank=True)
    used_referral = models.ForeignKey(ReferralCode, null=True, blank=True, on_delete=models.SET_NULL)
    def mark_purchased(self):
        self.purchased = True
        self.purchased_at = timezone.now()
        self.save()

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    passing_score = models.PositiveIntegerField(default=50)

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)
    correct = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

class Submission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    cert_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self): return f"Certificate {self.cert_id} for {self.user}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=100, unique=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)
    def __str__(self): return f"{self.user.username} - {self.course.title} - {self.ref}"

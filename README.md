
LearnPlatform - Full Django Starter (Paystack-ready)
===================================================

This project is a ready-to-run starter for an online learning platform (Udemy-like) with:
- User registration/login
- Course -> Modules -> Videos (video URL or upload)
- Enrollment/purchase flow with Paystack integration (placeholders)
- Exams per course, certificate generation
- Referral codes & simple analytics
- Admin dashboard view (superuser)
- Day / Night theme, hero homepage
- SQLite database for local dev

IMPORTANT (Paystack):
- Replace PAYSTACK_PUBLIC_KEY and PAYSTACK_SECRET_KEY in learnplatform/settings.py
  with your Paystack test/live keys before testing payments.
- Callback/redirect URLs: By default the callback is http://127.0.0.1:8000/paystack/verify/
  Configure Paystack dashboard when using production.

Quick start:
1. Extract the zip and `cd` into project root (where manage.py is).
2. Create & activate virtualenv:
   python -m venv venv
   # mac/linux
   source venv/bin/activate
   # windows (PowerShell)
   venv\Scripts\Activate.ps1
3. Install dependencies:
   pip install -r requirements.txt
4. Apply migrations and create superuser:
   python manage.py migrate
   python manage.py createsuperuser
5. (Optional) Load sample data:
   python manage.py loaddata initial_data.json
6. Run server:
   python manage.py runserver
7. Open http://127.0.0.1:8000/

Notes:
- This starter uses Paystack for payments. For production, secure keys and use HTTPS.

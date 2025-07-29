#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_site.settings')

    # 👇 Tạo superuser từ biến môi trường nếu chưa có
    if 'runserver' in sys.argv or 'gunicorn' in sys.argv or 'migrate' in sys.argv:
        try:
            import django
            django.setup()
            from django.contrib.auth import get_user_model

            username = os.getenv("DJANGO_SUPERUSER_USERNAME")
            email = os.getenv("DJANGO_SUPERUSER_EMAIL")
            password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

            if username and email and password:
                User = get_user_model()
                if not User.objects.filter(username=username).exists():
                    print("🚀 Tạo superuser tự động...")
                    User.objects.create_superuser(username=username, email=email, password=password)
                else:
                    print("✅ Superuser đã tồn tại.")
        except Exception as e:
            print(f"⚠️ Không thể tạo superuser: {e}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

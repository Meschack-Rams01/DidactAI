@echo off
echo 🔐 DidactAI Superuser Password Reset
echo =====================================
echo.
echo Found superuser: admin@didactia.com (username: admin)
echo.
echo Choose an option:
echo 1. Reset password using interactive script
echo 2. Use Django changepassword command
echo 3. Create a new superuser
echo.
set /p choice="Enter your choice (1-3): "

if %choice%==1 (
    echo.
    echo Running password reset script...
    python reset_admin_password.py
) else if %choice%==2 (
    echo.
    echo Using Django changepassword command...
    python manage.py changepassword admin
) else if %choice%==3 (
    echo.
    echo Creating a new superuser...
    python manage.py createsuperuser
) else (
    echo Invalid choice!
)

echo.
pause
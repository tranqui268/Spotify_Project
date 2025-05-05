from accounts.models import CustomUser

# Tạo user admin
admin_username = 'admin'
admin_email = 'admin@example.com'
admin_password = 'adminpassword123'

admin_user, created = CustomUser.objects.get_or_create(
    username=admin_username,
    defaults={
        'email': admin_email,
        'is_staff': True,
        'is_superuser': True,
        'is_premium': True,
    }
)
if created:
    admin_user.set_password(admin_password)
    admin_user.save()
    print('Created admin user: admin')
else:
    print('Admin user already exists')